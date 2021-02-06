
import pytest
from django_hosts.resolvers import reverse
from django.conf import settings
from radon.iot.tests import factories as iof
from radon.users.tests import factories as uf
from radon.georadon.tests import factories as geof
from radon.market.tests import factories as mktf
from radon.rutas.tests import factories as rutf
from radon.iot.tests import factories as iotf
from radon.rutas.models import Pedido
from radon.iot.models import Lectura

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
    response = tp.client.get(test_url, SERVER_NAME=FQN)
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
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_pedido_logged_ok(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('pedido', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


@pytest.mark.django_db
def test_app_dispositivo_detail_not_my_dispositivo_404(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('dispositivo_detail', kwargs={'serie': '123456'}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 404


@pytest.mark.django_db
def test_app_dispositivo_detail_my_dispositivo_ok(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('dispositivo_detail', kwargs={'serie': disp.wisol.serie}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert response.status_code == 200


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

# Probando contextos........
@pytest.mark.django_db
def test_dashboard_context(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('inicio', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert disp == response.context["dispositivo"]
    assert response.context["ultima_lectura"] is None


@pytest.mark.django_db
def test_graph_context(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)

    test_url = reverse('grafica', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)
    assert disp == response.context["dispositivo"]


@pytest.mark.django_db
def test_dispositivo_detail_context(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)
    rutf.PedidoFactory(dispositivo=disp)
    rutf.PedidoFactory(dispositivo=disp)
    pedido = rutf.PedidoFactory()
    iotf.LecturaFactory(dispositivo=disp)
    iotf.LecturaFactory(dispositivo=disp)
    iotf.LecturaFactory(dispositivo=pedido.dispositivo)
    pedidos = disp.pedido_set.all().select_related('precio').select_related('jornada').order_by('-jornada__fecha')
    lecturas = disp.lectura_set.order_by('-fecha')

    test_url = reverse('dispositivo_detail', kwargs={'serie': disp.wisol.serie}, host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)

    assert set(pedidos) == set(response.context["pedidos"])
    assert set(lecturas) == set(response.context["lecturas"])


@pytest.mark.django_db
def test_pedido_context(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)
    localidad_2 = geof.LocalidadFactory()
    precio = mktf.PrecioFactory(localidad=disp.localidad)
    mktf.PrecioFactory(localidad=localidad_2)

    test_arr = [
        {
         'sucursal_pk': precio.sucursal.pk,
         'gasera': precio.sucursal.gasera.nombre,
         'numeroPermiso': precio.sucursal.numeroPermiso,
         'telefono': precio.sucursal.telefono
        }
    ]

    test_url = reverse('pedido', host=HOST)
    response = tp.client.get(test_url, SERVER_NAME=FQN)

    assert [obj for obj in response.context["sucursales"]] == test_arr
    assert response.context["dispositivo"] == disp


@pytest.mark.django_db
def test_pedido_post_no_problem(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)
    precio = mktf.PrecioFactory(localidad=disp.localidad)

    data = {
         'cantidad': 1000,
         'dispositivo': disp.pk,
         'sucursal': precio.sucursal.pk
        }

    test_url = reverse('pedido', host=HOST)
    response = tp.client.post(test_url, data=data, SERVER_NAME=FQN)

    from django.contrib.messages import get_messages

    messages = [m.message for m in get_messages(response.wsgi_request)]
    mensajes_test = [
        'El pedido ha sido realizado.'
    ]

    pedido = Pedido.objects.last()

    assert pedido.dispositivo == disp
    assert pedido.cantidad == 1000
    assert messages == mensajes_test


@pytest.mark.django_db
def test_pedido_post_no_valid(tp):
    disp = do_user_dispositivo()
    tp.client.login(username=generic_username, password=generic_password)
    precio = mktf.PrecioFactory(localidad=disp.localidad)

    data = {
         'cantidad': '',
         'dispositivo': disp.pk,
         'sucursal': precio.sucursal.pk
        }

    test_url = reverse('pedido', host=HOST)
    response = tp.client.post(test_url, data=data, SERVER_NAME=FQN)

    from django.contrib.messages import get_messages

    messages = [m.message for m in get_messages(response.wsgi_request)]
    mensajes_test = [
        'Ha ocurrido un error con la solicitud, vuelve a intentarlo.'
    ]

    assert response.status_code == 302
    assert messages == mensajes_test
