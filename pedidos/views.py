from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, ListView, TemplateView

from usuarios.mixins import PersonalRequeridoMixin

from catalogo.models import Producto

from .carrito import Carrito
from .forms import EnvioForm
from .models import Pedido
from .servicios import PedidoError, crear_pedido, cambiar_estado


def _leer_cantidad(request, default=1):
    try:
        return int(request.POST.get("cantidad", default))
    except (TypeError, ValueError):
        return default


class CarritoView(TemplateView):
    template_name = "pedidos/carrito.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        carrito = Carrito(self.request)
        ctx["lineas"] = carrito.lineas()
        ctx["total"] = carrito.total
        return ctx


class AgregarView(View):
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk, activo=True)
        try:
            Carrito(request).agregar(producto, _leer_cantidad(request))
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("catalogo:detalle", pk=pk)
        messages.success(request, f"«{producto.nombre}» se agregó al carrito.")
        return redirect("pedidos:carrito")


class ActualizarView(View):
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        try:
            Carrito(request).actualizar(producto, _leer_cantidad(request))
            messages.success(request, "Carrito actualizado.")
        except ValueError as e:
            messages.error(request, str(e))
        return redirect("pedidos:carrito")


class QuitarView(View):
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        Carrito(request).quitar(producto)
        messages.info(request, f"«{producto.nombre}» se quitó del carrito.")
        return redirect("pedidos:carrito")


class VaciarView(View):
    def post(self, request):
        Carrito(request).vaciar()
        messages.info(request, "Carrito vaciado.")
        return redirect("pedidos:carrito")


class CarritoNoVacioMixin:
    """Si el carrito está vacío, manda de vuelta al carrito."""
    def dispatch(self, request, *args, **kwargs):
        if not Carrito(request):
            messages.warning(request, "Tu carrito está vacío.")
            return redirect("pedidos:carrito")
        return super().dispatch(request, *args, **kwargs)


class CheckoutView(LoginRequiredMixin, CarritoNoVacioMixin, FormView):
    template_name = "pedidos/checkout.html"
    form_class = EnvioForm
    success_url = reverse_lazy("pedidos:confirmar")

    def get_initial(self):
        initial = super().get_initial()
        envio = self.request.session.get("envio")
        if envio:
            initial.update(envio)
        else:
            initial["telefono_contacto"] = self.request.user.telefono
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        carrito = Carrito(self.request)
        ctx["lineas"] = carrito.lineas()
        ctx["total"] = carrito.total
        return ctx

    def form_valid(self, form):
        self.request.session["envio"] = form.cleaned_data
        return super().form_valid(form)


class ConfirmarView(LoginRequiredMixin, CarritoNoVacioMixin, TemplateView):
    template_name = "pedidos/confirmar.html"

    def get(self, request, *args, **kwargs):
        if "envio" not in request.session:
            return redirect("pedidos:checkout")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        carrito = Carrito(self.request)
        lineas = carrito.lineas()
        ctx["lineas"] = lineas
        ctx["total"] = carrito.total
        ctx["envio"] = self.request.session["envio"]
        ctx["hay_problemas"] = any(not l["disponible"] for l in lineas)
        return ctx

    def post(self, request, *args, **kwargs):
        envio = request.session.get("envio")
        if not envio:
            return redirect("pedidos:checkout")

        carrito = Carrito(request)
        try:
            pedido = crear_pedido(request.user, carrito, envio)
        except PedidoError as e:
            messages.error(request, str(e))
            return redirect("pedidos:carrito")

        carrito.vaciar()
        request.session.pop("envio", None)
        messages.success(request, f"¡Pedido #{pedido.pk} registrado con éxito!")
        return redirect("pedidos:detalle", pk=pedido.pk)


class PedidoDetailView(LoginRequiredMixin, DetailView):
    template_name = "pedidos/pedido_detalles.html"
    context_object_name = "pedido"

    def get_queryset(self):
        qs = Pedido.objects.select_related("usuario").prefetch_related("detalles__producto")
        if self.request.user.es_personal:
            return qs
        return qs.filter(usuario=self.request.user)


class PedidoListView(LoginRequiredMixin, ListView):
    template_name = "pedidos/pedido_list.html"
    context_object_name = "pedidos"
    paginate_by = 10

    def get_queryset(self):
        qs = Pedido.objects.select_related("usuario")
        user = self.request.user
        if not user.es_personal:
            return qs.filter(usuario=user)

        estado = self.request.GET.get("estado", "")
        if estado in Pedido.Estado.values:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estados"] = Pedido.Estado.choices
        estado = self.request.GET.get("estado", "")
        ctx["estado_actual"] = estado if estado in Pedido.Estado.values else ""
        return ctx


class CambiarEstadoView(PersonalRequeridoMixin, View):
    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        nuevo = request.POST.get("estado", "")
        try:
            cambiar_estado(pedido.pk, nuevo)
        except PedidoError as e:
            messages.error(request, str(e))
        else:
            if nuevo == Pedido.Estado.CANCELADO:
                messages.success(request, f"Pedido #{pk} cancelado. El stock fue repuesto.")
            else:
                messages.success(request, f"Pedido #{pk} actualizado.")
        return redirect("pedidos:detalle", pk=pk)