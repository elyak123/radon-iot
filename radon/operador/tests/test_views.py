import pytest
from django_hosts.resolvers import reverse
from django.conf import settings
from radon.iot.tests import factories as iof
from radon.users.tests import factories as uf

HOST = 'operador'
FQN = f'{HOST}.{settings.PARENT_HOST}'

generic_username = "job"
generic_password = "123inhackeable"


def do_operador():
    username = generic_username
    password = generic_password
    user = uf.OperadorFactory(username=username, password=password)
    return user


@pytest.mark.django_db
def test_operador_inicio_no_logged_redirect_login(tp):
    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302


@pytest.mark.django_db
def test_operador_creacion_usuario_no_logged_redirect_login(tp):
    test_url = reverse('creacion-usuario', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302


@pytest.mark.django_db
def test_operador_checar_email_get_method_not_allowed(tp):
    test_url = reverse('checar-email', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 405


@pytest.mark.django_db
def test_operador_inicio_logged_ok(tp):
    user = do_operador()
    tp.client.login(username=generic_username, password=generic_password)
    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_operador_creacion_usuario_logged_ok(tp):
    user = do_operador()
    tp.client.login(username=generic_username, password=generic_password)
    test_url = reverse('creacion-usuario', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_email_unique_no_problem(tp):
    data = {
         'email': 'chanchito@abc.com'
        }
    test_response = {'emailIsUnique': True}
    test_url = reverse('checar-email', host=HOST)
    response = tp.client.post(test_url, data=data, SERVER_NAME=FQN)
    assert response.data == test_response
    assert response.status_code == 200


@pytest.mark.django_db
def test_email_taken(tp):
    user = do_operador()
    data = {
         'email': user.email
        }
    test_url = reverse('checar-email', host=HOST)
    response = tp.client.post(test_url, data=data, SERVER_NAME=FQN)
    assert response.status_code == 400
