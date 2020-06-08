from django.shortcuts import render
from radon.users.auth import AuthenticationTestMixin
from django.views import generic

# Create your views here.
class DashboardView(AuthenticationTestMixin, generic.TemplateView):
    temlpate_name = "inicio.html"
