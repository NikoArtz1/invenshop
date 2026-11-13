from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PersonalRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):
    # Solo Empleado y Administrador. Sin sesión va a login; con sesión pero sin rol da 403

    def test_func(self):
        return self.request.user.es_personal