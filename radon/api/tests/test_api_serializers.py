from dj_rest_auth.utils import jwt_encode
from radon.api import serializers


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


def test_expiration_jwt_serializer_get_refesh_token(mocker): # FALLA
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


def test_ExpirationRefreshJWTSerializer_validation(mocker): # FALLA
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


def test_ExpirationRefreshJWTSerializer_validation_no_rotate(settings, mocker): # FALLA
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


def test_ExpirationRefreshJWTSerializer_rotate_no_blacklist(settings, mocker): # FALLA
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
