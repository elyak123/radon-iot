import pytz
import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from radon.users.tests import factories as user_factories
from radon.iot.tests import factories as iot_factories
from radon.rutas.tests import factories as rutas_factories
from radon.rutas.models import Pedido


class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DEBUG:
            call_command('flush')
            cantidad_gaseras = 10
            consumidores_por_gasera = 18
            vechiculos_por_gasera = 12
            jornadas_por_gasera = 30
            pedidos_por_usuario = int((vechiculos_por_gasera * jornadas_por_gasera) / consumidores_por_gasera)
            tz = pytz.timezone(settings.TIME_ZONE)
            gaseras = user_factories.GaseraFactory.create_batch(cantidad_gaseras)
            for index, gasera in enumerate(gaseras):
                usrs = user_factories.UserFactory.create_batch(
                    consumidores_por_gasera, gasera=gasera, tipo='CONSUMIDOR'
                )
                usuario_cliente = user_factories.UserFactory(gasera=gasera, tipo='CLIENTE')
                self.stdout.write(self.style.SUCCESS(
                    f'Usuario consumidor: {usrs[0].username}\n'
                    f'Usuario cliente: {usuario_cliente.username}\n'
                    f'Gasera: {gasera.nombre}\n'
                    '------------------------------------\n')
                )
                usrs[0].set_password('password')
                dt = iot_factories.DeviceTypeFactory()
                ws = iot_factories.WisolFactory.create_batch(consumidores_por_gasera, deviceTypeId=dt)
                vehiculos = rutas_factories.VehiculoFactory.create_batch(vechiculos_por_gasera, gasera=gasera)
                today = datetime.datetime.now()
                for day in range(jornadas_por_gasera):
                    fecha = today - datetime.timedelta(days=-day)
                    jornada = rutas_factories.JornadaFactory(gasera=gasera, fecha=fecha)
                    for vehiculo in vehiculos:
                        ruta = rutas_factories.RutaFactory(jornada=jornada)
                        ruta.vehiculo.add(vehiculo)
                for usr, wisol in zip(usrs, ws):
                    disp = iot_factories.DispositivoFactory(wisol=wisol, usuario=usr)
                    pds = rutas_factories.PedidoFactory.create_batch(pedidos_por_usuario, dispositivo=disp)
                    for pedido in pds:
                        Pedido.objects.filter(pk=pedido.pk).update(
                            fecha_creacion=rutas_factories.fake.date_time_this_month(tzinfo=tz)
                        )
        else:
            raise ImproperlyConfigured('No tienes settings.DEBUG activado, la operación no se puede completar.')
