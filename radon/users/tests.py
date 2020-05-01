import pytest
from pytest_django import asserts
from dj_rest_auth.utils import jwt_encode
from radon.users import serializers
from radon.users.models import User


def test_url_reverse_activacion_usuarios(tp):
    expected_url = '/users/activacion-usuarios/'
    reversed_url = tp.reverse('users:activacion-usuarios')
    assert expected_url == reversed_url


def test_url_reverse_user_dispositivo_registration(tp):
    expected_url = '/users/user-dispositivo-registration/'
    reversed_url = tp.reverse('users:usr-disp-reg')
    assert expected_url == reversed_url


def test_userserializer_calls_correct_method(mocker):
    create_user = mocker.patch('radon.users.models.User.objects.create_user')
    mock_user = mocker.MagicMock(spec=User)
    create_user.return_value = mock_user
    serializer = serializers.UserSerializer()
    usr = serializer.create({'username': 'bla'})
    User.objects.create_user.assert_called_once_with(**{'username': 'bla'})
    assert isinstance(usr, User) is True


def test_userserializer_sets_password_correctly(mocker):
    mocker.patch('rest_framework.serializers.ModelSerializer.update')
    usr = mocker.MagicMock()
    mock_set_pwd = mocker.MagicMock()
    usr.set_password = mock_set_pwd
    serializer = serializers.UserSerializer()
    serializer.update(usr, validated_data={'password': 'mypass'})
    usr.set_password.assert_called_once_with('mypass')


def test_userserializer_no_password(mocker):
    mocker.patch('rest_framework.serializers.ModelSerializer.update')
    usr = mocker.MagicMock()
    mock_set_pwd = mocker.MagicMock()
    usr.set_password = mock_set_pwd
    serializer = serializers.UserSerializer()
    serializer.update(usr, validated_data={'bla': 'xxxx'})
    usr.set_password.assert_not_called()


@pytest.mark.django_db
def test_userserializer_creates_user():
    data = {'username': 'myusername', 'email': 'my@user.com'}
    ser = serializers.UserSerializer(data=data)
    ser.is_valid()
    usr = ser.save()
    assert usr.has_usable_password() is False
    control_user = User.objects.get(email=data['email'])
    assert usr == control_user


def test_expiration_jwt_serializer_get_access_token(mocker):
    mock_user = mocker.patch('radon.users.models.User')
    mock_token_str = mocker.patch('rest_framework_simplejwt.tokens.Token.__str__')
    mock_token_str.return_value = 'foo'
    mock_user.id = 3
    access, refresh = jwt_encode(mock_user)
    refresh.payload['exp'] = 'today'
    access['exp'] = 'today'
    data = {'user': mock_user, 'access_token': access, 'refresh_token': refresh}
    ser = serializers.ExpirationJWTSerializer(instance=data)
    assert ser.get_access_token(data) == {'token': 'foo', 'exp': 'today'}


def test_expiration_jwt_serializer_get_refesh_token(mocker):
    mock_user = mocker.patch('radon.users.models.User')
    mock_token_str = mocker.patch('rest_framework_simplejwt.tokens.Token.__str__')
    mock_token_str.return_value = 'foo'
    mock_user.id = 3
    access, refresh = jwt_encode(mock_user)
    refresh.payload['exp'] = 'today'
    access['exp'] = 'today'
    data = {'user': mock_user, 'access_token': access, 'refresh_token': refresh}
    ser = serializers.ExpirationJWTSerializer(instance=data)
    assert ser.get_refresh_token(data) == {'token': 'foo', 'exp': 'today'}


def test_userserializer_is_valid(mocker):
    #  Asumimos que el username e email no existen
    mocker.patch('rest_framework.validators.UniqueValidator.__call__')
    usr_data = {
        'username': 'myuser', 'first_name': 'Myuser',
        'last_name': 'lastname', 'email': 'my@user.com', 'password': 'blabla'
    }
    ser = serializers.UserSerializer(data=usr_data)
    assert ser.is_valid() is True, ser.errors


def test_ExpirationRefreshJWTSerializer_validation(mocker):
    mock_refresh_klass = mocker.patch('radon.users.serializers.RefreshToken')
    mock_refresh = mocker.MagicMock()
    mock_refresh_klass.return_value = mock_refresh
    mock_refresh.__str__.return_value = 'foo__str__'
    mock_refresh.__getitem__.return_value = 'today'

    mock_refresh_blacklist = mocker.MagicMock()
    mock_refresh_blacklist.side_effect = AttributeError

    mock_access_token = mocker.MagicMock()

    mock_jti = mocker.MagicMock()

    mock_set_exp = mocker.MagicMock()

    mock_refresh.access_token = mock_access_token
    mock_refresh.blacklist = mock_refresh_blacklist
    mock_refresh.set_jti = mock_jti
    mock_refresh.set_exp = mock_set_exp

    # se llama str() debido a que el campo del serielizador es CharField
    data = {'refresh': str({'token': 'foo__str__', 'exp': 'today'})}
    ser = serializers.ExpirationRefreshJWTSerializer(data={'refresh': 'wkakakak'})
    ser.is_valid()
    mock_refresh_blacklist.assert_called_once_with()
    assert ser.data == data


def test_ExpirationRefreshJWTSerializer_validation_no_rotate(settings, mocker):
    settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS'] = False
    mock_refresh_klass = mocker.patch('radon.users.serializers.RefreshToken')
    mock_refresh = mocker.MagicMock()
    mock_refresh_klass.return_value = mock_refresh

    mock_access_token = mocker.MagicMock()
    mock_access_token.__str__.return_value = 'foo__str__'
    mock_access_token.__getitem__.return_value = 'today'

    mock_jti = mocker.MagicMock()

    mock_set_exp = mocker.MagicMock()

    mock_refresh.access_token = mock_access_token
    mock_refresh.set_jti = mock_jti
    mock_refresh.set_exp = mock_set_exp

    # se llama str() debido a que el campo del serielizador es CharField
    data = {'refresh': str({'token': 'foo__str__', 'exp': 'today', 'type': 'access'})}
    ser = serializers.ExpirationRefreshJWTSerializer(data={'refresh': 'wkakakak'})
    assert ser.is_valid() is True
    assert ser.data == data


def test_ExpirationRefreshJWTSerializer_rotate_no_blacklist(settings, mocker):
    settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS'] = True
    settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION'] = False
    mock_refresh_klass = mocker.patch('radon.users.serializers.RefreshToken')
    mock_refresh = mocker.MagicMock()
    mock_refresh.__str__.return_value = 'foo__str__'
    mock_refresh.__getitem__.return_value = 'today'
    mock_refresh_klass.return_value = mock_refresh
    mock_refresh_blacklist = mocker.MagicMock()
    mock_refresh_blacklist.side_effect = AttributeError
    mock_refresh.blacklist = mock_refresh_blacklist
    mock_set_jti = mocker.MagicMock()
    mock_refresh.set_jti = mock_set_jti
    mock_set_exp = mocker.MagicMock()
    mock_refresh.set_exp = mock_set_exp
    data = {'refresh': str({'token': 'foo__str__', 'exp': 'today'})}
    ser = serializers.ExpirationRefreshJWTSerializer(data={'refresh': 'wkakakak'})
    assert ser.is_valid() is True
    mock_refresh_blacklist.assert_not_called()
    mock_set_jti.assert_called_once_with()
    mock_set_exp.assert_called_once_with()
    assert ser.data == data
