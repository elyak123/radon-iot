import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker
from django.contrib.auth import get_user_model
from unidecode import unidecode
from radon.market.tests.factories import SucursalFactory
from radon.users.models import Consumidor, Operador, Staff

User = get_user_model()
fake = Faker(['es_MX'])
faker = Faker(['es_MX', 'en_US', 'it_IT', 'fr_FR'])


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(
        lambda o: unidecode(o.first_name.split(' ')[0].lower() + '_' + o.last_name.lower()))
    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    telefono = factory.LazyAttribute(lambda o: fake.numerify(fake.random_element(('####-###-###',))))
    last_name = factory.LazyAttribute(lambda o: faker.last_name())
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username, fake.domain_name()))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    tipo = FuzzyChoice(['CLIENTE', 'CONSUMIDOR', 'STAFF', 'OPERARIO'])

    class Meta:
        model = User
        django_get_or_create = ('username',)


class ConsumidorFactory(UserFactory):
    class Meta:
        model = Consumidor
        django_get_or_create = ('username',)


class OperadorFactory(UserFactory):
    class Meta:
        model = Operador
        django_get_or_create = ('username',)


class StaffFactory(UserFactory):
    class Meta:
        model = Staff
        django_get_or_create = ('username',)


class UserConsumidorSucursalFactory(UserFactory):
    sucursal = factory.SubFactory(SucursalFactory)
    tipo = 'CONSUMIDOR'

    class Meta:
        model = User
        django_get_or_create = ('username',)


class UserClientFactory(UserFactory):
    sucursal = factory.SubFactory(SucursalFactory)
    tipo = 'CLIENTE'

    class Meta:
        model = User
        django_get_or_create = ('username',)
