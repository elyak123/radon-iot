
from django_hosts.resolvers import reverse
import pytest

HOST = 'app'


@pytest.mark.django_db
def test_app_inicio_no_logged_redirect_login(tp):
    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_registro_ok(tp):
    test_url = reverse('register', host=HOST)
    import pdb; pdb.set_trace()
    response = tp.client.get(test_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_pedido_no_logged_redirect_login(tp):
    test_url = reverse('pedido', host=HOST)
    response = tp.client.get(test_url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_dispositivo_detail_no_logged_redirect_login(tp):
    test_url = reverse('dispositivo_detail', args=(1,), host=HOST)
    response = tp.client.get(test_url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_app_pedidos_no_logged_redirect_login(tp):
    test_url = reverse('pedidos', host=HOST)
    response = tp.client.get(test_url)
    assert response.status_code == 302
