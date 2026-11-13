from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Usuario

class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs.setdefault("class", "form-control")


class RegistroForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("email", "first_name", "last_name", "telefono")
        labels = {
            "email": "Email",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "telefono": "Teléfono",
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese email.")
        return email

class LoginForm(BootstrapMixin, AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )

class PerfilForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "telefono")
        labels = {"first_name": "Nombre", "last_name": "Apellido", "telefono": "Teléfono"}