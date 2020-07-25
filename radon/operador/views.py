from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "operador/inicio.html"


class CreacionUsuarioView(LoginRequiredMixin, generic.FormView):
    template_name = "operador/creacion-usuario.html"

