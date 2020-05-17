from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from radon.users.auth import AuthenticationTestMixin
from radon.iot.models import Dispositivo

# Create your views here.


class DashboardView(TemplateView, AuthenticationTestMixin):
    template_name = "dashboard/index.html"


class DispositivoListView(ListView):
    model = Dispositivo
    template_name = "dashboard/dispositivo_list.html"

    def get_queryset(self):
        query = self.model.objects.filter(
            usuario__gasera=self.request.user.gasera
        )
        return query
