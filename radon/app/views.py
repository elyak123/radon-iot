from django.views import generic
from rest_framework.response import Response
from rest_framework import status
from radon.users.auth import AuthenticationTestMixin


class DashboardView(generic.TemplateView):
    template_name = "app/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['ultima_lectura'] = {'lectura': self.request.user.dispositivo_set.first().get_ultima_lectura()}
        return context


def sigfox(request):
    return Response({}, status.HTTP_204_NO_CONTENT)


class GraphView(generic.TemplateView):
    template_name = "app/grafica.html"
