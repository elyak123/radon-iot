import factory
from faker import Faker
from radon.market import models
fake = Faker(['es_MX'])
faker = Faker(['es_MX', 'en_US', 'it_IT', 'fr_FR'])


class GaseraFactory(factory.django.DjangoModelFactory):
    nombre = factory.LazyAttribute(lambda o: '{} {}'.format(fake.company(), fake.company_suffix()))

    class Meta:
        model = models.Gasera
        django_get_or_create = ('nombre',)


class SucursalFactory(factory.django.DjangoModelFactory):
    numeroPermiso = factory.LazyAttribute(lambda o: f'LP/{fake.numerify(text="#####")}/DIST/PLA/{fake.year()}')
    gasera = factory.SubFactory(GaseraFactory)


class PrecioFactory(factory.django.DjangoModelFactory):
    precio = factory.LazyAttribute(lambda o: fake.random_int(min=9, max=18))
    sucursal = factory.SubFactory(SucursalFactory)

    class Meta:
        model = models.Precio
        django_get_or_create = ('precio', 'sucursal')
