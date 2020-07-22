from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "app/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['ultima_lectura'] = {'lectura': self.request.user.dispositivo_set.first().get_ultima_lectura()}
        return context


class GraphView(generic.TemplateView):
    template_name = "app/grafica.html"
