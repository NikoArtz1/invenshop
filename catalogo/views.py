from django.shortcuts import render

from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Categoria, Producto

class ProductoListView(ListView):
    model = Producto
    template_name = "catalogo/producto_list.html"
    context_object_name = "productos"
    paginate_by = 12

    def get_queryset(self):
        qs = Producto.objects.filter(activo = True).select_related("categoria")

        q = self.request.GET.get("q", "").strip()
        categoria = self.request.GET.get("categoria", "")
        orden = self.request.GET.get("orden", "nombre")

        if q:
            qs = qs.filter(Q(nombre__icontains = q) | Q(descripcion__icontains = q))

        if categoria: 
            qs = qs.filter(categoria__slug = categoria)

        if orden not in ("nombre", "precio", "-precio"):
            orden = "nombre"

        return qs.order_by(orden) 

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.all()

        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = params.urlencode()

        return ctx

class ProductoDetailView(DetailView):
    model = Producto
    template_name = "catalogo/producto_detail.html"
    context_object_name = "producto"

    def get_queryset(self):
        return Producto.objects.filter(activo=True).select_related("categoria")