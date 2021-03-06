from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django_hosts.resolvers import reverse
from radon.georadon.models import Localidad
from radon.market.models import Sucursal
from radon.iot.models import Dispositivo
from radon.rutas.models import Pedido
from radon.users.auth import ConsumidorAutenticationMixin
from django.conf import settings


class BaseTemplateSelector(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template"] = 'app/base.html'
        return context


class AppAuthBaseClass(ConsumidorAutenticationMixin, BaseTemplateSelector):
    pass


class DashboardView(AppAuthBaseClass, generic.TemplateView):
    template_name = "app/inicio.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        dispositivos = self.request.user.dispositivo_set.all()
        context['dispositivos'] = []
        context['ultimas_lecturas'] = []
        context['litros'] = []
        context['indexes'] = []
        i = 0
        for dispositivo in dispositivos:
            lectura = dispositivo.get_ultima_lectura() if dispositivo else None
            if lectura:
                lectura['counter'] = "nivelLectura" + str(i)
                context['dispositivos'].append(dispositivo)
                context['ultimas_lecturas'].append(lectura)
                context['litros'].append(round(dispositivo.capacidad * (lectura['lectura']/100), 0))
                context['indexes'].append(i)
                i = i + 1
        return context


class RegisterView(BaseTemplateSelector, generic.TemplateView):
    template_name = "app/creacion-usuario.html"


class RegistroDispositivo(BaseTemplateSelector, generic.TemplateView):
    template_name = "app/creacion-dispositivo.html"


class PedidosView(AppAuthBaseClass, generic.TemplateView):
    template_name = "app/pedidos.html"

    def get_context_data(self, **kwargs):
        context = super(PedidosView, self).get_context_data(**kwargs)
        dispositivos = self.request.user.dispositivo_set.all()
        context['dispositivos'] = dispositivos
        return context


class PedidoDetailView(AppAuthBaseClass, generic.DetailView):
    template_name = "app/detalle-pedido.html"
    model = Pedido


class PedidoView(AppAuthBaseClass, generic.TemplateView):
    template_name = "app/pedido.html"

    def get_context_data(self, **kwargs):
        context = super(PedidoView, self).get_context_data(**kwargs)
        dispositivo = self.request.user.dispositivo_set.get(wisol__serie=self.kwargs['serie'])
        context['dispositivo'] = dispositivo
        localidad = Localidad.objects.filter(geo__intersect=dispositivo.location.wkt) if not dispositivo.localidad else dispositivo.localidad  # noqa: E501
        context['sucursales'] = Sucursal.especial.from_localidad(localidad)
        return context

    def post(self, request, *args, **kwargs):
        datos = self.request.POST
        pedido = Pedido(
            cantidad=datos["cantidad"],
            dispositivo=Dispositivo.objects.get(id=datos["dispositivo"]),
            precio=Sucursal.objects.get(id=datos["sucursal"]).precio_set.last()
        )
        try:
            pedido.full_clean()
        except ValidationError:
            messages.warning(request, "Ha ocurrido un error con la solicitud, vuelve a intentarlo.")
            return redirect(reverse('pedido', host=self.request.host.regex))
        pedido.save()
        messages.success(request, "El pedido ha sido realizado.")
        return redirect(reverse('inicio', host=self.request.host.regex))


class GraphView(AppAuthBaseClass, generic.TemplateView):
    template_name = "app/grafica.html"

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
        dispositivo = self.request.user.dispositivo_set.get(wisol__serie=self.kwargs['serie'])
        context['dispositivo'] = dispositivo
        return context


class DispositivoDetailView(AppAuthBaseClass, generic.DetailView):
    model = Dispositivo
    template_name = "app/dispositivo_detail.html"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            self.model,
            wisol__serie=self.kwargs['serie'],
            usuario=self.request.user
        )
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lecturas"] = self.object.lecturas_ordenadas()[:10]
        context["pedidos"] = self.object.pedidos_ordenados()[:10]
        return context


def asset_links(req):
    respuesta = [{
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {"namespace": "android_app", "package_name": "com.radargas.app.twa",
                 "sha256_cert_fingerprints": [settings.PLAYSTORE_APP_KEY]}
    }]
    return JsonResponse(respuesta, safe=False)
