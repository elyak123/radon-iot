from django.conf import settings
from django_hosts.resolvers import reverse
HOST = 'api'
FQN = f'{HOST}.{settings.PARENT_HOST}'


def test_url_reverse_activacion_usuarios_on_api(tp):
    expected_url = f'//{FQN}/users/activacion-usuarios/'
    reversed_url = reverse('activacion-usuarios', host=HOST)
    assert expected_url == reversed_url


def test_url_reverse_user_dispositivo_registration(tp):
    expected_url = f'//{FQN}/users/user-dispositivo-registration/'
    reversed_url = reverse('usr-disp-reg', host=HOST)
    assert expected_url == reversed_url


# reverse de django hosts, ahi indico el host para que agarre los namespaces del subdominio.
# consultar en users views y accounts views.