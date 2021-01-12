from django_hosts.resolvers import reverse
from django.views import generic
from django.http import JsonResponse
from radon.users.auth import AuthenticationTestMixin
from radon.users.models import User
from radon.iot.models import Dispositivo
from radon.rutas.models import Pedido, Jornada
from radon.iot.forms import DispositivoForm
from datetime import datetime
import json

from radon.rutas.forms import PedidoCreationForm
from radon.app.views import BaseTemplateSelector

# Create your views here.


class DashboardView(AuthenticationTestMixin, generic.TemplateView, BaseTemplateSelector):
    pass


class JornadaView(AuthenticationTestMixin, generic.DetailView, BaseTemplateSelector):
    template_name = "crm/index.html"
    model = Jornada

    def get_object(self, queryset=None):
        now = datetime.now()
        self.object = self.model.objects.get(fecha=now, gasera=self.request.user.gasera)
        return self.object

    def get_context_data(self, **kwargs):
        context = super(JornadaView, self).get_context_data(**kwargs)
        if not self.object.geometria_actualizada:
            pass  # aqui va la peticion...
        context['dispositivos'] = Dispositivo.especial.calendarizados_geojson(self.object)
        context['rutas'] = self.object.rutas_geojson()
        return context


def get_geojsons(request, fecha):
    obj = {}
    jornada = Jornada.objects.get(
        fecha=fecha,
        gasera=request.user.gasera
    )
    obj['dispositivos'] = json.loads(
        Dispositivo.especial.calendarizados_geojson(
            jornada
        )
    )
    obj['rutas '] = json.loads(
        jornada.rutas_geojson()
    )
    return JsonResponse(obj)


class DispositivoListView(AuthenticationTestMixin, generic.ListView, BaseTemplateSelector):
    paginate_by = 10
    model = Dispositivo
    template_name = "crm/dispositivo_list.html"

    def get_queryset(self):
        query = self.model.especial.filter(
            usuario__gasera=self.request.user.gasera
        ).select_related('wisol').select_related('usuario').anotar_lecturas().order_by('ultima_lectura')
        return query


class DispositivoCriticoListView(DispositivoListView, BaseTemplateSelector):
    template_name = "crm/leads.html"

    def get_queryset(self):
        query = User.especial.leads(self.request.user.gasera)
        return query


class DispositivoDetailView(generic.DetailView, BaseTemplateSelector):
    model = Dispositivo
    template_name = "crm/dispositivo_detail.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.select_related('usuario').select_related('wisol').get(
            wisol__serie=self.kwargs['serie'],
            # usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lecturas"] = self.object.lecturas_ordenadas()[:10]
        context["pedidos"] = self.object.pedidos_ordenados()[:10]
        return context

    def get_success_url(self):
        return reverse('crm:dispositivo_detail', kwargs={'pk': self.object.pk})


class DispositivoUpdateView(generic.UpdateView, BaseTemplateSelector):
    form_class = DispositivoForm
    model = Dispositivo
    template_name = "crm/dispositivo_update.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            wisol__serie=self.kwargs['serie'],
            usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('dispositivo_detail', kwargs={'serie': self.object.wisol.serie}, host='crm')


class DispositivoDeleteView(AuthenticationTestMixin, generic.DeleteView, BaseTemplateSelector):
    model = Dispositivo
    template_name = "crm/dispositivo_delete.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            wisol__serie=self.kwargs['serie'],
            usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('crm:dispositivo_list', kwargs={'pk': self.object.pk})


class PedidoView(generic.TemplateView, BaseTemplateSelector):
    template_name = "crm/pedidos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        if not kwargs["week"]:
            context["semana"] = f"{now.year}-W{now.isocalendar()[1]}"
        else:
            context["semana"] = kwargs["week"]
        context["pedidos"] = Pedido.especial.pedidos_por_dia_por_gasera(
            gasera=self.request.user.gasera,
            semana=context["semana"]
        )
        return context


class PedidoCreateView(generic.CreateView, BaseTemplateSelector):
    model = Pedido
    form_class = PedidoCreationForm
    template_name = "crm/pedido_creation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dispositivo"] = Dispositivo.objects.get(
            wisol__serie=self.kwargs["dispositivo"],
            usuario__gasera=self.request.user.gasera
        )
        context['gasera'] = self.request.user.gasera
        now = datetime.now()
        context["current_week"] = f"{now.year}-W{now.isocalendar()[1]}"
        if not self.kwargs.get("week"):
            context["week"] = context["current_week"]
        else:
            context["week"] = self.kwargs["week"]
        context["pedidos"] = Pedido.especial.pedidos_por_dia_por_gasera(
            gasera=self.request.user.gasera,
            semana=context["week"]
        )
        context["now"] = datetime.now().date()
        return context

    def get_initial(self):
        initial_obj = super(PedidoCreateView, self).get_initial()
        dispositivo = Dispositivo.objects.get(
            wisol__serie=self.kwargs["dispositivo"],
            usuario__gasera=self.request.user.gasera
        )
        precio = self.request.user.gasera.precio_actual
        initial_obj["dispositivo"] = dispositivo
        initial_obj["precio"] = precio
        return initial_obj

    def get_success_url(self):
        return reverse('crm:histograma_pedidos')
