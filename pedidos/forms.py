import re

from django import forms
from usuarios.forms import BootstrapMixin
from .models import Pedido

class EnvioForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ("direccion", "ciudad", "codigo_postal", "telefono_contacto")
        labels = {
            "direccion": "Dirección",
            "ciudad": "Ciudad",
            "codigo_postal": "Código postal",
            "telefono_contacto": "Teléfono de contacto",
        }

    #Usamos expresiones regulares para que el texto coincida con lo que se pide
    def clean_direccion(self):
        direccion = self.cleaned_data["direccion"].strip()
        if len(direccion) < 5:
            raise forms.ValidationError("Ingresá una dirección completa (calle y altura).")
        if not any(c.isdigit() for c in direccion) and "s/n" not in direccion.lower():
            raise forms.ValidationError("Incluí la altura de la calle (o «S/N» si no tiene).")
        return direccion

    def clean_ciudad(self):
        ciudad = self.cleaned_data["ciudad"].strip()
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ .'\-]{2,}", ciudad):
            raise forms.ValidationError("La ciudad solo puede tener letras, espacios y guiones.")
        return ciudad

    def clean_codigo_postal(self):
        cp = self.cleaned_data["codigo_postal"].strip().upper()
        if not re.fullmatch(r"\d{4}|[A-Z]\d{4}[A-Z]{3}", cp):
            raise forms.ValidationError(
                "Código postal inválido. Usá 4 dígitos (4200) o formato CPA (G4200ABC)."
            )
        return cp

    def clean_telefono_contacto(self):
        telefono = self.cleaned_data["telefono_contacto"].strip()
        if not re.fullmatch(r"\+?[\d\s\-()]+", telefono):
            raise forms.ValidationError("El teléfono solo puede tener números, espacios, + - ( ).")
        if not 8 <= len(re.sub(r"\D", "", telefono)) <= 15:
            raise forms.ValidationError("El teléfono debe tener entre 8 y 15 dígitos.")
        return telefono