from django.views import generic
from radon.users.auth import AuthenticationTestMixin


class DashboardView(generic.TemplateView):
    template_name = "app/inicio.html"

    # def get_context_data(self, **kwargs):
    #     context = super(DashboardView, self).get_context_data(**kwargs)
    #     context['ultima_lectura'] = {'lectura': self.request.user.dispositivo_set.first().get_ultima_lectura()}
    #     return context


class GraphView(generic.TemplateView):
    template_name = "app/grafica.html"
