from django.conf import settings
from django.http.request import HttpRequest
from django_hosts.resolvers import reverse
from rest_framework.response import Response
import pytest
from test_plus.test import CBVTestCase
from radon.users.tests.factories import ConsumidorFactory, UserClientFactory
from radon.api import views
from radon.api import serializers

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
def test_permission_checkAPILeadsView_consumdor_denied(client):
    usr = ConsumidorFactory(password='123inhackeable')
    test_url = reverse('leads', host=HOST)
    client.login(username=usr.username, password='123inhackeable')
    request = client.get(test_url, SERVER_NAME=FQN)
    assert request.status_code == 403


@pytest.mark.django_db
def test_permission_checkAPILeadsView_200_cliente(client, mocker):
    mocker.patch('radon.users.views.LeadsView.get_queryset')
    usr = UserClientFactory(password='123inhackeable')
    test_url = reverse('leads', host=HOST)
    client.login(username=usr.username, password='123inhackeable')
    request = client.get(test_url, SERVER_NAME=FQN)
    assert request.status_code == 200
