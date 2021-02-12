import pytz
import factory
from faker import Faker
from django.contrib.auth import get_user_model
from django.conf import settings
from radon.users.tests.factories import UserFactory, StaffFactory
from radon.market.tests.factories import PrecioFactory, SucursalFactory
from radon.iot.tests.factories import DispositivoFactory
from radon.rutas import models

User = get_user_model()
fake = Faker(['es_MX'])
tz = pytz.timezone(settings.TIME_ZONE)


class JornadaFactory(factory.django.DjangoModelFactory):
    fecha = factory.LazyAttribute(lambda o: fake.date_this_month())
    sucursal = factory.SubFactory(SucursalFactory)

    class Meta:
        model = models.Jornada


class VehiculoFactory(factory.django.DjangoModelFactory):
    placa = factory.LazyAttribute(lambda o: fake.license_plate())
    n_economico = factory.LazyAttribute(lambda o: fake.bothify(text='?? ##'))
    operador = factory.SubFactory(UserFactory, tipo='OPERARIO')
    sucursal = factory.SubFactory(SucursalFactory)
    capacidad = factory.LazyAttribute(lambda o: fake.random_element(elements=[5000, 8500, 12500]))

    class Meta:
        model = models.Vehiculo


class RutaFactory(factory.django.DjangoModelFactory):
    jornada = factory.SubFactory(JornadaFactory)
    geometry = 'LINESTRING(0 0,1 1,1 2)'

    @factory.post_generation
    def pedidos_set(obj, create, extracted, **kwargs):
        if extracted:
            ls = 'LINESTRING('
            for pedido in extracted:
                ls + '{} {},'.format(pedido.dispositivo.location.x, pedido.dispositivo.location.x)
            ls + ')'
            obj.geometry = ls
            obj.save()

    class Meta:
        model = models.Ruta


class PedidoFactory(factory.django.DjangoModelFactory):
    fecha_creacion = factory.LazyAttribute(lambda o: fake.date_time_this_month())
    cantidad = factory.LazyAttribute(lambda o: fake.random_int(min=10, max=150))
    dispositivo = factory.SubFactory(DispositivoFactory)
    precio = factory.SubFactory(PrecioFactory)

    class Meta:
        model = models.Pedido


class MensajeFactory(factory.django.DjangoModelFactory):
    autor = factory.SubFactory(StaffFactory)
    texto = factory.fuzzy.FuzzyText(length=10)
    pedido = factory.SubFactory(PedidoFactory)
    publicacion = factory.LazyAttribute(lambda o: fake.date_time_this_month(tzinfo=tz))

    class Meta:
        model = models.Mensaje
