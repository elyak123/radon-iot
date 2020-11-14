import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker
from django.contrib.auth import get_user_model
from radon.users.models import Gasera, Precio
from unidecode import unidecode

User = get_user_model()
fake = Faker(['es_MX'])
faker = Faker(['es_MX', 'en_US', 'it_IT', 'fr_FR'])


class GaseraFactory(factory.django.DjangoModelFactory):
    nombre = factory.LazyAttribute(lambda o: '{} {}'.format(fake.company(), fake.company_suffix()))

    class Meta:
        model = Gasera
        django_get_or_create = ('nombre',)


class PrecioFactory(factory.django.DjangoModelFactory):
    precio = factory.LazyAttribute(lambda o: fake.random_int(min=9, max=18))
    gasera = factory.SubFactory(GaseraFactory)

    class Meta:
        model = Precio
        django_get_or_create = ('precio', 'gasera')


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(
        lambda o: unidecode(o.first_name.split(' ')[0].lower() + '_' + o.last_name.lower()))
    # lambda o: fake.first_name().split(' ')[0].lower() + '_' + fake.lexify())
    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    telefono = factory.LazyAttribute(lambda o: fake.numerify(fake.random_element(('####-###-###',))))
    last_name = factory.LazyAttribute(lambda o: faker.last_name())
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username, fake.domain_name()))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    gasera = factory.SubFactory(GaseraFactory)
    tipo = FuzzyChoice(['CLIENTE', 'CONSUMIDOR', 'STAFF', 'OPERARIO'])

    class Meta:
        model = User
        # django_get_or_create = ('username',)
