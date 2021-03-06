import factory
from faker import Faker
from radon.georadon import models
from radon.georadon.tests.fuzz import FuzzyMultiPolygon

fake = Faker(['es_MX'])


class EstadoFactory(factory.django.DjangoModelFactory):
    nombre = factory.LazyAttribute(lambda o: fake.state())

    class Meta:
        model = models.Estado
        django_get_or_create = ('nombre',)


class MunicipioFactory(factory.django.DjangoModelFactory):
    clave = factory.LazyAttribute(lambda o: f'{fake.numerify(text="#####")}')
    nombre = factory.LazyAttribute(lambda o: f'{fake.city()}')
    estado = factory.SubFactory(EstadoFactory)
    geo = FuzzyMultiPolygon(tipo='municipio', length=15)

    class Meta:
        model = models.Municipio
        django_get_or_create = ('nombre',)


class LocalidadFactory(factory.django.DjangoModelFactory):
    geo = factory.LazyAttribute(
        lambda o: FuzzyMultiPolygon(tipo='localidad', length=30, centroid=o.municipio.geo.centroid).fuzz()
    )
    nombre = factory.LazyAttribute(lambda o: fake.address().split('\n')[1].split(',')[0])
    clave = factory.LazyAttribute(lambda o: f'{fake.numerify(text="#####")}')
    municipio = factory.SubFactory(MunicipioFactory)

    class Meta:
        model = models.Localidad
        django_get_or_create = ('clave',)
