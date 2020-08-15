from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "app/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        dispositivo = self.request.user.dispositivo_set.first()
        lectura = dispositivo.get_ultima_lectura() if dispositivo else None
        context['ultima_lectura'] = lectura
        return context


class GraphView(generic.TemplateView):
    template_name = "app/grafica.html"
