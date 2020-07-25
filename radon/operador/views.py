from django.shortcuts import render

# Create your views here.
class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "operador/inicio.html"
