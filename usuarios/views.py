from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, PerfilForm, RegistroForm


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("usuarios:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("catalogo:lista")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Cuenta creada. Ya podés iniciar sesión.")
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "usuarios/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        siguiente = self.get_redirect_url()
        if siguiente:
            return siguiente
        if self.request.user.es_personal:
            return reverse("admin:index")
        return reverse("catalogo:lista")


class PerfilView(LoginRequiredMixin, UpdateView):
    form_class = PerfilForm
    template_name = "usuarios/perfil.html"
    success_url = reverse_lazy("usuarios:perfil")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado.")
        return super().form_valid(form)


class CambiarPasswordView(PasswordChangeView):
    template_name = "usuarios/cambiar_password.html"
    success_url = reverse_lazy("usuarios:perfil")

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada.")
        return super().form_valid(form)