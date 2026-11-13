from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("registro/", views.RegistroView.as_view(), name="registro"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("perfil/", views.PerfilView.as_view(), name="perfil"),
    path("perfil/password/", views.CambiarPasswordView.as_view(), name="cambiar_password"),
]