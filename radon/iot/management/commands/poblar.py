import pytz
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
            tz = pytz.timezone(settings.TIME_ZONE)
            gaseras = user_factories.GaseraFactory.create_batch(10)
            for index, gasera in enumerate(gaseras):
                usrs = user_factories.UserFactory.create_batch(15, gasera=gasera, tipo='CONSUMIDOR')
                usuario_cliente = user_factories.UserFactory(gasera=gasera, tipo='CLIENTE')
                self.stdout.write(self.style.SUCCESS(
                    f'Usuario consumidor: {usrs[0].username}\n'
                    f'Usuario cliente: {usuario_cliente.username}\n'
                    f'Gasera: {gasera.nombre}\n'
                    '------------------------------------\n')
                )
                usrs[0].set_password('password')
                dt = iot_factories.DeviceTypeFactory()
                ws = iot_factories.WisolFactory.create_batch(15, deviceTypeId=dt)
                for usr, wisol in zip(usrs, ws):
                    iot_factories.DispositivoFactory(wisol=wisol, usuario=usr)
                    rutas_factories.PedidoFactory.create_batch(20, dispositivo__usuario=usr)
                    Pedido.objects.filter(dispositivo__usuario=usr).update(
                        fecha_creacion=rutas_factories.fake.date_time_this_month(tzinfo=tz))
                rutas_factories.VehiculoFactory.create_batch(12, gasera=gasera)
        else:
            raise ImproperlyConfigured('No tienes settings.DEBUG activado, la operación no se puede completar.')
