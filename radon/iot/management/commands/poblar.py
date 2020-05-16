from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from radon.users.tests import factories as user_factories
from radon.iot.tests import factories as iot_factories
from radon.rutas.tests import factories as rutas_factories


class Command(BaseCommand):

    def handle(self, *args, **options):
        if settings.DEBUG:
            call_command('flush')
            gaseras = user_factories.GaseraFactory.create_batch(10)
            for index, gasera in enumerate(gaseras):
                usrs = user_factories.UserFactory.create_batch(40, gasera=gasera, tipo='CONSUMIDOR')
                self.stdout.write(self.style.SUCCESS(
                    f'username: {usrs[0].username}\nGasera: {gasera.nombre}'
                    '\n--------------\n')
                )
                usrs[0].set_password('password')
                dt = iot_factories.DeviceTypeFactory()
                ws = iot_factories.WisolFactory.create_batch(40, deviceTypeId=dt)
                for usr, wisol in zip(usrs, ws):
                    iot_factories.DispositivoFactory(wisol=wisol, usuario=usr)
                rutas_factories.VehiculoFactory.create_batch(12, gasera=gasera)
        else:
            raise ImproperlyConfigured('No tienes settings.DEBUG activado, la operación no se puede completar.')
