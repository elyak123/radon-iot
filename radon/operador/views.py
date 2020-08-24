from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from radon.iot.models import Instalacion
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from radon.users import serializers
from radon.app.views import BaseTemplateSelector


class DashboardView(LoginRequiredMixin, generic.ListView, BaseTemplateSelector):
    template_name = "operador/listado_instalaciones.html"
    model = Instalacion
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(operario=self.request.user).order_by('-fecha')


class CreacionUsuarioView(LoginRequiredMixin, generic.TemplateView, BaseTemplateSelector):
    template_name = "operador/creacion-usuario.html"


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ChecarEmailView(request):
    serializer = serializers.EmailValidator(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'emailIsUnique': True}, status.HTTP_200_OK, {})
