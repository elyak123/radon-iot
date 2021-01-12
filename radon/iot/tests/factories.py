import factory
from faker import Faker
from django.contrib.auth import get_user_model
from radon.iot import models
from radon.users.tests.factories import UserFactory
from radon.georadon.tests.factories import MunicipioFactory

User = get_user_model()
fake = Faker(['es_MX'])


class DeviceTypeFactory(factory.django.DjangoModelFactory):
    key = factory.LazyAttribute(lambda o: fake.hexify())
    name = factory.LazyAttribute(lambda o: fake.bothify('????-########'))

    class Meta:
        model = models.DeviceType
        django_get_or_create = ('key',)


class WisolFactory(factory.django.DjangoModelFactory):
    serie = fake.numerify(text='43#####')
    serie = factory.LazyAttribute(lambda o: fake.numerify(text='43#####'))
    pac = factory.LazyAttribute(lambda o: fake.hexify(text='^^^^^^^^^^^^^^^^', upper=True))
    prototype = factory.LazyAttribute(lambda o: fake.boolean())
    deviceTypeId = factory.SubFactory(DeviceTypeFactory)

    class Meta:
        model = models.Wisol
        django_get_or_create = ('serie',)


class DispositivoFactory(factory.django.DjangoModelFactory):
    wisol = factory.SubFactory(WisolFactory)
    capacidad = factory.LazyAttribute(lambda o: fake.random_element(
        elements=[120, 300, 500, 1000, 1600, 2200, 2800, 3400, 5000]
    ))
    usuario = factory.SubFactory(UserFactory)
    location = factory.LazyAttribute(
        lambda o: 'POINT({} {})'.format(
            fake.coordinate(center=o.municipio.geo.centroid.x, radius=0.07),
            fake.coordinate(center=o.municipio.geo.centroid.y, radius=0.05)
            )
        )
    municipio = factory.SubFactory(MunicipioFactory)

    class Meta:
        model = models.Dispositivo
        django_get_or_create = ('wisol',)


class InstalacionFactory(factory.django.DjangoModelFactory):
    fecha = factory.LazyAttribute(lambda o: fake.date_this_month())
    operario = factory.SubFactory(UserFactory, tipo='OPERARIO')
    consumidor = factory.SubFactory(UserFactory, tipo='CONSUMIDOR')

    class Meta:
        model = models.Instalacion


class LecturaFactory(factory.django.DjangoModelFactory):
    fecha = factory.LazyAttribute(lambda o: fake.date_this_month())
    nivel = factory.LazyAttribute(lambda o: fake.random_int(min=15, max=87))
    dispositivo = factory.SubFactory(DispositivoFactory)

    class Meta:
        model = models.Lectura
