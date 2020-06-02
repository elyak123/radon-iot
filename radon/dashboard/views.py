from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from radon.users.auth import AuthenticationTestMixin
from radon.iot.models import Dispositivo
from radon.rutas.models import Pedido, Jornada
from radon.iot.forms import DispositivoForm
from datetime import datetime
import json

from radon.rutas.forms import PedidoCreationForm

# Create your views here.


class DashboardView(AuthenticationTestMixin, generic.TemplateView):
    pass


class JornadaView(AuthenticationTestMixin, generic.DetailView):
    template_name = "dashboard/index.html"
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


class DispositivoListView(AuthenticationTestMixin, generic.ListView):
    paginate_by = 10
    model = Dispositivo
    template_name = "dashboard/dispositivo_list.html"

    def get_queryset(self):
        query = self.model.especial.filter(
            usuario__gasera=self.request.user.gasera
        ).select_related('wisol').select_related('usuario').anotar_lecturas().order_by('ultima_lectura')
        return query


class DispositivoDetailView(AuthenticationTestMixin, generic.DetailView):
    model = Dispositivo
    template_name = "dashboard/dispositivo_detail.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            pk=self.kwargs['pk'],
            usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('dashboard:dispositivo_detail', kwargs={'pk': self.object.pk})


class DispositivoUpdateView(AuthenticationTestMixin, generic.UpdateView):
    form_class = DispositivoForm
    model = Dispositivo
    template_name = "dashboard/dispositivo_update.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            pk=self.kwargs['pk'],
            usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('dashboard:dispositivo_detail', kwargs={'pk': self.object.pk})


class DispositivoDeleteView(AuthenticationTestMixin, generic.DeleteView):
    model = Dispositivo
    template_name = "dashboard/dispositivo_delete.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            pk=self.kwargs['pk'],
            usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('dashboard:dispositivo_list', kwargs={'pk': self.object.pk})


class PedidoView(AuthenticationTestMixin, generic.TemplateView):
    template_name = "dashboard/pedidos.html"

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


class PedidoCreateView(AuthenticationTestMixin, generic.CreateView):
    model = Pedido
    form_class = PedidoCreationForm
    template_name = "dashboard/pedido_creation.html"

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
        return reverse('dashboard:histograma_pedidos')
