import factory
from faker import Faker
from django.contrib.auth import get_user_model
from radon.users.tests.factories import UserFactory, GaseraFactory
from radon.iot.tests.factories import DispositivoFactory
from radon.rutas import models

User = get_user_model()
fake = Faker(['es_MX'])


class JornadaFactory(factory.django.DjangoModelFactory):
    fecha = fake.date_this_month()
    gasera = factory.SubFactory(GaseraFactory)

    class Meta:
        model = models.Jornada


class VehiculoFactory(factory.django.DjangoModelFactory):
    placa = fake.license_plate()
    n_economico = fake.bothify(text='?? ##')
    operador = factory.SubFactory(UserFactory, tipo='OPERADOR')

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
    fecha_creacion = fake.date_this_month()
    cantidad = fake.random_int(min=30, max=100)
    dispositivo = factory.SubFactory(DispositivoFactory)

    class Meta:
        model = models.Pedido
