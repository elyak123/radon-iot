import pytz
import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from radon.users.tests import factories as user_factories
from radon.iot.models import Wisol, Dispositivo
from radon.iot.tests import factories as iot_factories
from radon.rutas.tests import factories as rutas_factories
from radon.rutas.models import Pedido


class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DEBUG:
            call_command('flush')
            cantidad_gaseras = 4
            consumidores_por_gasera = 18
            vechiculos_por_gasera = 12
            jornadas_por_gasera = 30
            pedidos_por_ruta = 8
            cantidad_wisol = cantidad_gaseras * consumidores_por_gasera
            pedidos_por_usuario = int(
                (jornadas_por_gasera * vechiculos_por_gasera * pedidos_por_ruta) / consumidores_por_gasera)
            tz = pytz.timezone(settings.TIME_ZONE)
            gaseras = user_factories.GaseraFactory.create_batch(cantidad_gaseras)
            iot_factories.WisolFactory.create_batch(cantidad_wisol)
            for index, gasera in enumerate(gaseras):
                precio = user_factories.PrecioFactory(gasera=gasera)
                usrs = user_factories.UserFactory.create_batch(
                    consumidores_por_gasera, gasera=gasera, tipo='CONSUMIDOR'
                )
                usuario_cliente = user_factories.UserFactory(gasera=gasera, tipo='CLIENTE')
                ws = Wisol.objects.filter(dispositivo__isnull=True)
                for usr, wisol in zip(usrs, ws):
                    disp = iot_factories.DispositivoFactory(wisol=wisol, usuario=usr)
                    rutas_factories.PedidoFactory.create_batch(
                        # ¿Aqui?
                        pedidos_por_usuario, dispositivo=disp, jornada=None, ruta=None, orden=None, precio=precio
                    )
                vehiculos = rutas_factories.VehiculoFactory.create_batch(vechiculos_por_gasera, gasera=gasera)
                today = datetime.datetime.now()
                for day in range(1, jornadas_por_gasera + 1):
                    fecha = today + datetime.timedelta(days=+day)
                    jornada = rutas_factories.JornadaFactory(gasera=gasera, fecha=fecha)
                    for vehiculo in vehiculos:
                        ruta = rutas_factories.RutaFactory(jornada=jornada)
                        ruta.vehiculo.add(vehiculo)
                        for idx in range(pedidos_por_ruta):
                            # ¿Aqui?
                            ped = Pedido.objects.filter(
                                dispositivo__usuario__gasera=gasera,
                                ruta__isnull=True
                                ).order_by('-fecha_creacion').first()
                            if ped:
                                ped.jornada = jornada
                                # ¿Aqui?
                                ped.ruta = ruta
                                ped.orden = idx
                                ped.save()
                                ped.dispositivo.calendarizado = True
                                ped.dispositivo.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Usuario consumidor: {usrs[0].username}\n'
                    f'Usuario cliente: {usuario_cliente.username}\n'
                    f'Gasera: {gasera.nombre}\n'
                    '------------------------------------\n')
                )
            pedidos_global = Pedido.objects.all().values('pk')
            for pd in pedidos_global:
                Pedido.objects.filter(pk=pd['pk']).update(
                    fecha_creacion=rutas_factories.fake.date_time_this_month(tzinfo=tz)
                )
        else:
            raise ImproperlyConfigured('No tienes settings.DEBUG activado, la operación no se puede completar.')
