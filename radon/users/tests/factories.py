import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker
from django.contrib.auth import get_user_model
from radon.users.models import Gasera

User = get_user_model()
fake = Faker(['es_MX'])


class GaseraFactory(factory.django.DjangoModelFactory):
    nombre = factory.LazyAttribute(lambda o: '{} {}'.format(fake.company(), fake.company_suffix()))

    class Meta:
        model = Gasera
        django_get_or_create = ('nombre',)


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda o: o.first_name.split(' ')[0].lower())
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username, fake.domain_name()))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    gasera = factory.SubFactory(GaseraFactory)
    tipo = FuzzyChoice(['CLIENTE', 'CONSUMIDOR', 'STAFF', 'OPERARIO'])

    class Meta:
        model = User
        django_get_or_create = ('username',)
