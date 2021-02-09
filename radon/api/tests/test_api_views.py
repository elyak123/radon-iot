from django.conf import settings
from django.http.request import HttpRequest
from rest_framework.response import Response
import pytest
from test_plus.test import CBVTestCase
from radon.api import views
from radon.api import serializers

HOST = 'api'
FQN = f'{HOST}.{settings.PARENT_HOST}'


def test_APIUsersLoginView_response_serializer(tp):
    view = CBVTestCase.get_instance(views.APIUsersLoginView)
    ser = view.get_response_serializer()
    assert serializers.ExpirationJWTSerializer == ser


@pytest.mark.django_db
def test_api_activacion_usuarios_calls_users_app_func(tp_api, mocker):
    mock_view = mocker.patch('radon.api.views.userviews.activacion_usuarios')
    mock_view.return_value = Response({}, 200, {})
    mock_permission = mocker.patch('radon.api.views.drf_permissions.IsAuthenticated.has_permission')
    mock_permission.return_value = True
    rq = HttpRequest()
    rq.method = 'POST'
    views.api_activacion_usuarios(rq)
    mock_view.assert_called_once()
    mock_permission.assert_called_once()
