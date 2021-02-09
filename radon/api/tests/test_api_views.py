from radon.api import views
from radon.api import serializers
from test_plus.test import CBVTestCase


def test_APIUsersLoginView_response_serializer(tp):
    view = CBVTestCase.get_instance(views.APIUsersLoginView)
    ser = view.get_response_serializer()
    assert serializers.ExpirationJWTSerializer == ser


# def test_api_activacion_usuarios_calls_users_app_func(tp, mocker):
#     mocker.patch('radon.api.views.userviews.activacion_usuarios')
#     view = CBVTestCase.get_instance(views.api_activacion_usuarios)
    
