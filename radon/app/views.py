from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin


class BaseTemplateSelector(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = 'base.html'
        if hasattr(self.request.user, 'tipo'):
            if self.request.user.tipo == 'OPERARIO':
                template = 'operador/base.html'
            elif self.request.user.tipo == 'CONSUMIDOR':
                template = 'app/base.html'
            elif self.request.user.tipo == 'CLIENTE':
                template = 'cambiar template'
        context["template"] = template
        return context
    

class DashboardView(LoginRequiredMixin, BaseTemplateSelector, generic.TemplateView):
    template_name = "app/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        dispositivo = self.request.user.dispositivo_set.first()
        lectura = dispositivo.get_ultima_lectura() if dispositivo else None
        context['dispositivo'] = dispositivo
        context['ultima_lectura'] = lectura
        return context


class RegisterView(BaseTemplateSelector, generic.TemplateView):
    template_name = "app/creacion-usuario.html"
    

class PedidoView(BaseTemplateSelector, generic.TemplateView):
    template_name = "app/pedido.html"
    
    def get_context_data(self, **kwargs):
        context = super(PedidoView, self).get_context_data(**kwargs)
        dispositivo = self.request.user.dispositivo_set.first()
        context['dispositivo'] = dispositivo
        return context


class GraphView(generic.TemplateView, BaseTemplateSelector):
    template_name = "app/grafica.html"
    
    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
        dispositivo = self.request.user.dispositivo_set.first()
        context['dispositivo'] = dispositivo
        return context
