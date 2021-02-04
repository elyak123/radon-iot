import json
from datetime import datetime
from django_hosts.resolvers import reverse
from django.views import generic
from django.http import JsonResponse
from radon.users.auth import ClienteAutenticationMixin
from radon.users.models import Cliente
from radon.iot.models import Dispositivo
from radon.rutas.models import Pedido, Jornada
from radon.iot.forms import DispositivoForm
from radon.rutas.forms import PedidoCreationForm


class CrmTemplateSelector(ClienteAutenticationMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template"] = 'crm/base.html'
        return context


class JornadaView(CrmTemplateSelector, generic.DetailView):
    """
    De momento sin url, su implementacion esta pendiente.
    """
    template_name = "crm/index.html"
    model = Jornada

    def get_object(self, queryset=None):
        now = datetime.now()
        self.object = self.model.objects.get(fecha=now, sucursal=self.request.user.sucursal)
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
        sucursal=request.user.sucursal
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


class DispositivoListView(CrmTemplateSelector, generic.ListView):
    paginate_by = 10
    model = Dispositivo
    template_name = "crm/dispositivo_list.html"

    def get_queryset(self):
        query = self.model.especial.filter(
            sucursal=self.request.user.sucursal
        ).select_related('wisol').select_related('usuario').anotar_lecturas().order_by('ultima_lectura')
        return query


class DispositivoCriticoListView(DispositivoListView):
    template_name = "crm/leads.html"

    def get_queryset(self):
        query = Cliente.objects.leads(self.request.user.sucursal)
        return query


class DispositivoDetailView(CrmTemplateSelector, generic.DetailView):
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


class DispositivoUpdateView(CrmTemplateSelector, generic.UpdateView):
    form_class = DispositivoForm
    model = Dispositivo
    template_name = "crm/dispositivo_update.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            wisol__serie=self.kwargs['serie'],
            usuario__sucursal=self.request.user.sucursal
        )
        return self.object

    def get_success_url(self):
        return reverse('dispositivo_detail', kwargs={'serie': self.object.wisol.serie}, host='crm')


class DispositivoDeleteView(CrmTemplateSelector, generic.DeleteView):
    model = Dispositivo
    template_name = "crm/dispositivo_delete.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            wisol__serie=self.kwargs['serie'],
            usuario__sucursal=self.request.user.sucursal
        )
        return self.object

    def get_success_url(self):
        return reverse('crm:dispositivo_list', kwargs={'pk': self.object.pk})


class PedidoView(CrmTemplateSelector, generic.TemplateView):
    template_name = "crm/pedidos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = datetime.now()
        if not kwargs["week"]:
            context["semana"] = f"{now.year}-W{now.isocalendar()[1]}"
        else:
            context["semana"] = kwargs["week"]
        context["pedidos"] = Pedido.especial.pedidos_por_dia_por_gasera(
            sucursal=self.request.user.sucursal,
            semana=context["semana"]
        )
        return context


class PedidoCreateView(CrmTemplateSelector, generic.CreateView):
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
