from django.shortcuts import render
from radon.users.auth import AuthenticationTestMixin
from django.views import generic

# Create your views here.
class DashboardView(generic.TemplateView):
    template_name = "app/inicio.html"

class GraphView(generic.TemplateView):
    template_name = "app/grafica.html"
