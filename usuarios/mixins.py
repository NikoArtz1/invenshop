from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PersonalRequeridoMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.es_personal