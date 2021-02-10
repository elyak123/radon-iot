from django.conf import settings
from django.http.request import HttpRequest
from django_hosts.resolvers import reverse
from rest_framework.response import Response
from rest_framework.test import force_authenticate
import pytest
from test_plus.test import CBVTestCase
from radon.users.tests.factories import ConsumidorFactory
from radon.api import views
from radon.api import serializers
from radon.api import permissions

HOST = 'api'
FQN = f'{HOST}.{settings.PARENT_HOST}'


def test_APIUsersLoginView_response_serializer(tp):
    view = CBVTestCase.get_instance(views.APIUsersLoginView)
    ser = view.get_response_serializer()
    assert serializers.ExpirationJWTSerializer == ser


@pytest.mark.django_db
def test_api_activacion_usuarios_calls_users_app_func(mocker):
    mock_view = mocker.patch('radon.api.views.userviews.activacion_usuarios')
    mock_view.return_value = Response({}, 200, {})
    mock_permission = mocker.patch('radon.api.views.drf_permissions.IsAuthenticated.has_permission')
    mock_permission.return_value = True
    rq = HttpRequest()
    rq.method = 'POST'
    views.api_activacion_usuarios(rq)
    mock_view.assert_called_once()
    mock_permission.assert_called_once()


@pytest.mark.django_db
def test_api_localidades_dispositivos(mocker):
    mock_view = mocker.patch('radon.api.views.geoviews.localidades_dispositivos')
    mock_view.return_value = Response(status=200)
    mock_permission = mocker.patch('radon.api.views.drf_permissions.IsAdminUser.has_permission')
    mock_permission.return_value = True
    rq = HttpRequest()
    rq.method = 'GET'
    views.localidades_dispositivos(rq)
    mock_view.assert_called_once()
    mock_permission.assert_called_once()


@pytest.mark.django_db
def test_permission_checkAPILeadsView(tp):
    usr = ConsumidorFactory(password='123inhackeable')
    test_url = reverse('leads', host=HOST)
    tp.login(username=usr.username, password='123inhackeable')
    request = tp.client.get(test_url, SERVER_NAME=FQN)
    import pdb; pdb.set_trace()
    force_authenticate(request, user=usr)
