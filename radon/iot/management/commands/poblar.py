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
from radon.market.tests import factories as market_factories
from radon.rutas.models import Pedido, Jornada
from radon.market.models import Sucursal
from radon.contrib.sites.utils import create_sites


class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DEBUG:
            call_command('flush', '--noinput')
            call_command('createsu')
            create_sites()
            cantidad_gaseras = 1
            sucursales_por_gasera = 3
            vechiculos_por_sucursal = 6
            pedidos_por_ruta = 5
            vehiculos_por_gasera = vechiculos_por_sucursal * sucursales_por_gasera
            consumidores_por_sucursal = vechiculos_por_sucursal * pedidos_por_ruta
            consumidores_por_gasera = consumidores_por_sucursal * sucursales_por_gasera
            jornadas_por_sucursal = consumidores_por_sucursal
            cantidad_wisol = cantidad_gaseras * consumidores_por_sucursal * sucursales_por_gasera
            tz = pytz.timezone(settings.TIME_ZONE)
            gaseras = market_factories.GaseraFactory.create_batch(cantidad_gaseras)
            iot_factories.WisolFactory.create_batch(cantidad_wisol)
            # consumidores libres sin gasera
            user_factories.UserFactory.create_batch(consumidores_por_gasera, tipo='CONSUMIDOR')
            for gasera in gaseras:
                market_factories.SucursalFactory.create_batch(sucursales_por_gasera, gasera=gasera)
            sucursales = Sucursal.objects.all()
            for index, sucursal in enumerate(sucursales):
                precio = market_factories.PrecioFactory(sucursal=sucursal)
                consumidores = user_factories.UserConsumidorSucursalFactory.create_batch(
                    consumidores_por_sucursal, tipo='CONSUMIDOR', sucursal=sucursal
                )
                usuario_cliente = user_factories.UserClientFactory(sucursal=sucursal)
                ws = Wisol.objects.filter(dispositivo__isnull=True)
                today = datetime.datetime.now()
                for usr, wisol in zip(consumidores, ws):
                    disp = iot_factories.DispositivoFactory(wisol=wisol, usuario=usr, sucursal=sucursal)
                    # nivel_base = 85
                    # for day in range(10):
                    #     fecha = today - datetime.timedelta(days=+day)
                    #     iot_factories.LecturaFactory(dispositivo=disp, fecha=fecha, nivel=nivel_base)
                    #     nivel_base = nivel_base - 7
                vehiculos = rutas_factories.VehiculoFactory.create_batch(vehiculos_por_gasera, sucursal=sucursal)
                for day in range(jornadas_por_sucursal + 1):
                    fecha = today + datetime.timedelta(days=+day)
                    jornada = rutas_factories.JornadaFactory(sucursal=sucursal, fecha=fecha)
                    for vehiculo in vehiculos:
                        ruta = rutas_factories.RutaFactory(jornada=jornada)
                        ruta.vehiculo.add(vehiculo)
                jornadas = Jornada.objects.filter(sucursal=sucursal).order_by('fecha')
                dispositivos = Dispositivo.objects.filter(usuario__sucursal=sucursal)
                for idx, jor in enumerate(jornadas):
                    for dis in dispositivos:
                        rutas_factories.PedidoFactory(
                            dispositivo=dis, jornada=jor,
                            actualizado=True, orden=idx, precio=precio
                        )
                        dis.calendarizado = True
                        dis.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Usuario consumidor: {consumidores[0].username}\n'
                    f'Usuario cliente: {usuario_cliente.username}\n'
                    f'Gasera: {sucursal.gasera.nombre}\n'
                    f'Sucursal: {sucursal.municipio.nombre}\n'
                    '------------------------------------\n')
                )
            pedidos_global = Pedido.objects.all().values('pk')
            for pd in pedidos_global:
                Pedido.objects.filter(pk=pd['pk']).update(
                    fecha_creacion=rutas_factories.fake.date_time_this_month(tzinfo=tz)
                )
        else:
            raise ImproperlyConfigured('No tienes settings.DEBUG activado, la operación no se puede completar.')
