from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from radon.iot.models import Instalacion


class DashboardView(LoginRequiredMixin, generic.ListView):
    template_name = "operador/listado_instalaciones.html"
    model = Instalacion
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(operario=self.request.user).order_by('-fecha')
