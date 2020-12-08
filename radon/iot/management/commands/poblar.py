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
from radon.rutas.models import Pedido, Jornada
from radon.contrib.sites.utils import create_sites


class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DEBUG:
            call_command('flush', '--noinput')
            create_sites()
            cantidad_gaseras = 1
            vehiculos_por_gasera = 6
            pedidos_por_ruta = 5
            consumidores_por_gasera = vehiculos_por_gasera * pedidos_por_ruta
            jornadas_por_gasera = consumidores_por_gasera
            cantidad_wisol = cantidad_gaseras * consumidores_por_gasera
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
                    iot_factories.DispositivoFactory(wisol=wisol, usuario=usr)
                vehiculos = rutas_factories.VehiculoFactory.create_batch(vehiculos_por_gasera, gasera=gasera)
                today = datetime.datetime.now()
                for day in range(jornadas_por_gasera + 1):
                    fecha = today + datetime.timedelta(days=+day)
                    jornada = rutas_factories.JornadaFactory(gasera=gasera, fecha=fecha)
                    for vehiculo in vehiculos:
                        ruta = rutas_factories.RutaFactory(jornada=jornada)
                        ruta.vehiculo.add(vehiculo)
                jornadas = Jornada.objects.filter(gasera=gasera)
                dispositivos = Dispositivo.objects.filter(usuario__gasera=gasera)
                for idx, jor in enumerate(jornadas):
                    for dis in dispositivos:
                        rutas_factories.PedidoFactory(
                            dispositivo=dis, jornada=jor,
                            actualizado=True, orden=idx, precio=precio
                        )
                        dis.calendarizado = True
                        dis.save()
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
