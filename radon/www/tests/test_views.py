import pytest
from django_hosts.resolvers import reverse
from django.conf import settings


HOST = 'www'
FQN = f'{HOST}.{settings.PARENT_HOST}'

generic_username = "job"
generic_password = "123inhackeable"


@pytest.mark.django_db
def test_inicio_web_anonymous_access(tp):
    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_preguntas_frecuentes_web_anonymous_access(tp):
    test_url = reverse('preguntas', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200
