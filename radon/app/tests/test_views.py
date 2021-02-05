
import pytest
from django_hosts.resolvers import reverse
from django.conf import settings
from radon.iot.tests import factories as iof
from radon.users.tests import factories as uf

HOST = 'app'
FQN = f'{HOST}.{settings.PARENT_HOST}'

generic_username = "job"
generic_password = "123inhackeable"


def do_user_dispositivo():
    username = generic_username
    password = generic_password
    user = uf.ConsumidorFactory(username=username, password=password)
    disp = iof.DispositivoFactory(usuario=user)
    return disp


@pytest.mark.django_db
def test_app_inicio_no_logged_redirect_login(tp):
    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_registro_ok(tp):
    test_url = reverse('register', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_pedido_no_logged_redirect_login(tp):
    test_url = reverse('pedido', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_dispositivo_detail_no_logged_redirect_login(tp):
    test_url = reverse('dispositivo_detail', kwargs={'serie': '45234'}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_pedidos_no_logged_redirect_login(tp):
    test_url = reverse('pedidos', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_pedido_detail_no_logged_redirect_login(tp):
    test_url = reverse('detalle-pedido', kwargs={'pk': 1}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_checar_email_method_not_allowed(tp):
    test_url = reverse('checar-email', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 405


@pytest.mark.django_db
def test_app_grafica_redirect_login(tp):
    user = uf.ConsumidorFactory()
    disp = iof.DispositivoFactory(usuario=user)
    test_url = reverse('grafica', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 302

# Vistas should 200.
@pytest.mark.django_db
def test_app_inicio_logged_ok(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_pedido_logged_ok(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('pedido', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_dispositivo_detail_not_my_dispositivo_unauthorized(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('dispositivo_detail', kwargs={'serie': '45234'}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 403


@pytest.mark.django_db
def test_app_pedidos_logged_ok(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('pedidos', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_pedido_detail_logged_not_found(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('detalle-pedido', kwargs={'pk': 1}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 404


@pytest.mark.django_db
def test_app_grafica_ok(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('grafica', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200
