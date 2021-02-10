import pytest
from radon.iot.models import Dispositivo, Wisol, DeviceType
from radon.users import serializers
from radon.users.models import User
from radon.users.tests.factories import ConsumidorFactory
from radon.market.models import Sucursal
from radon.market.tests.factories import SucursalFactory
from radon.georadon.tests.factories import LocalidadFactory
from radon.georadon.models import Localidad, Municipio


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


def test_userserializer_is_valid(mocker):
    #  Asumimos que el username e email no existen
    mocker.patch('rest_framework.validators.UniqueValidator.__call__')
    usr_data = {
        'username': 'myuser', 'first_name': 'Myuser',
        'last_name': 'lastname', 'email': 'my@user.com', 'password': 'blabla'
    }
    ser = serializers.UserSerializer(data=usr_data)
    assert ser.is_valid() is True, ser.errors


def test_AsistedUserDispositivoCreation_validate_email_exists(mocker):
    email_validator = mocker.patch('radon.users.serializers.email_address_exists')
    email_validator.return_value = True
    ser = serializers.AsistedUserDispositivoCreation()
    with pytest.raises(serializers.serializers.ValidationError):
        ser.validate_email('yo@correo.com')
    email_validator.assert_called_once_with('yo@correo.com')


def test_AsistedUserDispositivoCreation_validate_email_not_exists(mocker):
    email_validator = mocker.patch('radon.users.serializers.email_address_exists')
    email_validator.return_value = False
    ser = serializers.AsistedUserDispositivoCreation()
    assert ser.validate_email('yo@correo.com') == 'yo@correo.com'
    email_validator.assert_called_once_with('yo@correo.com')


def test_AsistedUserDispositivoCreation_validate_email_not_unique_required(mocker):
    email_unique_validator = mocker.patch('radon.users.serializers.allauth_settings')
    email_unique_validator.UNIQUE_EMAIL = False
    email_validator = mocker.patch('radon.users.serializers.email_address_exists')
    ser = serializers.AsistedUserDispositivoCreation()
    assert ser.validate_email('yo@correo.com') == 'yo@correo.com'
    email_validator.assert_not_called()


def test_AsistedUserDispositivoCreation_validate_gasera(mocker):
    mock_request = mocker.MagicMock()
    mock_user = mocker.MagicMock(spec=User)
    mock_sucursal = mocker.MagicMock(spec=Sucursal)
    mock_sucursal.pk = 1
    mock_sucursal.id = 1
    mock_user.sucursal = mock_sucursal
    mock_request.user = mock_user
    context = {'request': mock_request}
    ser = serializers.AsistedUserDispositivoCreation(context=context)
    sucursal = ser.validate_sucursal('DUMMY')
    assert sucursal == mock_sucursal
    assert isinstance(sucursal, Sucursal) is True


def test_AsistedUserDispositivoCreation_validate_gasera_None(mocker):
    mock_request = mocker.MagicMock()
    mock_user = mocker.MagicMock(spec=User)
    del mock_user.sucursal
    mock_request.user = mock_user
    context = {'request': mock_request}
    ser = serializers.AsistedUserDispositivoCreation(context=context)
    sucursal = ser.validate_sucursal('DUMMY')
    assert sucursal is None


def test_AsistedUserDispositivoCreation_validate_username(mocker):
    #  Asumimos que el username no existe
    get_adapter = mocker.patch('radon.users.serializers.get_adapter')
    adapter = mocker.MagicMock()
    get_adapter.return_value = adapter
    clean_username = mocker.MagicMock()
    clean_username.return_value = 'waka'
    adapter.clean_username = clean_username
    ser = serializers.AsistedUserDispositivoCreation()
    assert ser.validate_username('waka') == 'waka'


def test_AsistedUserDispositivoCreation_get_cleaned_data(mocker):
    email_validator = mocker.patch('radon.users.serializers.email_address_exists')
    email_validator.return_value = False
    #  Asumimos que el username no existe
    get_adapter = mocker.patch('radon.users.serializers.get_adapter')
    mock_loc = mocker.MagicMock(spec=Localidad)
    moc_municipio = mocker.MagicMock(spec=Municipio)
    mock_sucursal = mocker.MagicMock(spec=Sucursal)
    mock_wkt = mocker.patch('radon.users.serializers.get_localidad_from_wkt', return_value=mock_loc)
    mock_loc.municipio = moc_municipio
    adapter = mocker.MagicMock()
    get_adapter.return_value = adapter
    clean_username = mocker.MagicMock()
    clean_username.return_value = 'waka'
    adapter.clean_username = clean_username
    ser = serializers.AsistedUserDispositivoCreation()
    ser.wisol = '41235'
    ser._validated_data = {
        'username': 'bla', 'email': 'yo@yo.com', 'tipo': 'CONSUMIDOR', 'pwdtemporal': True,
        'sucursal': mock_sucursal, 'location': 'POINT(133.1234 -122.344)', 'capacidad': 123
    }
    control_user = {
        'username': 'bla', 'email': 'yo@yo.com', 'tipo': 'CONSUMIDOR', 'pwdtemporal': True,
    }
    contorl_disp = {
        'location': 'POINT(133.1234 -122.344)',
        'capacidad': 123, 'wisol': '41235',
        'sucursal': mock_sucursal,
        'localidad': mock_loc, 'municipio': moc_municipio
    }
    assert ser.get_cleaned_data() == (control_user, contorl_disp)
    mock_wkt.assert_called_once_with('POINT(133.1234 -122.344)')


def test_AsistedUserDispositivoCreation_save(mocker):
    usr = mocker.MagicMock(spec=User)
    disp = mocker.MagicMock(spec=Dispositivo)
    req = mocker.MagicMock()
    get_cleaned_data = mocker.patch.object(serializers.AsistedUserDispositivoCreation, 'get_cleaned_data')
    create_user_and_dispositivo = mocker.patch('radon.users.serializers.create_user_and_dispositivo')
    create_user_and_dispositivo.return_value = usr, disp
    user_data = mocker.MagicMock()
    disp_data = mocker.MagicMock()
    get_cleaned_data.return_value = user_data, disp_data
    ser = serializers.AsistedUserDispositivoCreation()
    user = ser.save(req)
    assert isinstance(user, User) is True
    get_cleaned_data.assert_called_once_with()
    create_user_and_dispositivo.assert_called_once_with(user_data, disp_data)


@pytest.mark.django_db
def test_AsistedUserDispositivoCreation_with_db(mocker):
    dt = DeviceType.objects.create(key='bla', name='lnkasn')
    wisol = serializers.Wisol.objects.create(serie='41245', pac='kalks', deviceTypeId=dt)
    data = {
        'username': 'Joe', 'email': 'email@bla.com', 'telefono': '3312345622',
        'location': 'POINT(122.123455 -133.1235)', 'capacidad': 122, 'wisol': wisol.serie
    }
    req = mocker.MagicMock()
    req.user.sucursal = SucursalFactory()
    context = {'request': req}
    loc = LocalidadFactory()
    mocker.patch('radon.users.serializers.get_localidad_from_wkt', return_value=loc)
    ser = serializers.AsistedUserDispositivoCreation(data=data, context=context)
    assert ser.is_valid() is True
    user = ser.save(req)
    assert isinstance(user, User) is True
    assert user.has_usable_password() is False
    assert isinstance(user.pk, int) is True


def test_Temporal_Pass_User(mocker):
    mock_super_rep = mocker.patch('radon.users.serializers.AsistedUserDispositivoCreation.to_representation')
    mock_super_rep.return_value = {}
    mock_create_user_pass = mocker.patch('radon.users.serializers.create_user_password')
    mock_loc = mocker.patch('radon.users.serializers.get_localidad_from_wkt')
    mock_loc.return_value = mocker.MagicMock(spec=Localidad)
    mock_create_user_pass.return_value = 'blabla'
    usr = mocker.MagicMock(password='blabla')
    data = {
        'username': usr.username, 'email': usr.email, 'telefono': '3312345622',
        'location': 'POINT(122.123455 -133.1235)', 'capacidad': 122, 'wisol': '41235'
    }
    req = mocker.MagicMock()
    req.user.sucursal = mocker.MagicMock(spec=Sucursal)
    context = {'request': req}
    ser = serializers.TemporalPassUserDispsitivoCreation(data=data, context=context)
    ser.wisol = '41235'
    ser._validated_data = data
    ser.get_cleaned_data()
    rep = ser.to_representation(usr)
    assert rep['password'] == 'blabla'
    mock_create_user_pass.assert_called_once_with()
    mock_super_rep.assert_called_once()
    mock_loc.assert_called_once_with('POINT(122.123455 -133.1235)')


def test_ActivateUsers_validate_email_doesnot_exist(mocker):
    get_user = mocker.patch.object(User.objects, 'get')
    get_user.side_effect = User.DoesNotExist
    ser = serializers.ActivateUsers()
    with pytest.raises(serializers.serializers.ValidationError):
        ser.validate_email('yo@micasa.com')


def test_ActivateUsers_validate_email_does_exist(mocker):
    get_user = mocker.patch.object(User.objects, 'get')
    mock_user = mocker.MagicMock(spec=User)
    mock_user.pwdtemporal = True
    mock_user.is_active = True
    get_user.return_value = mock_user
    ser = serializers.ActivateUsers()
    email = ser.validate_email('yo@micasa.com')
    assert email == 'yo@micasa.com'


def test_ActivateUsers_validate_email_does_exist_pwdtemporal(mocker):
    get_user = mocker.patch.object(User.objects, 'get')
    mock_user = mocker.MagicMock(spec=User)
    mock_user.pwdtemporal = False
    mock_user.is_active = True
    get_user.return_value = mock_user
    ser = serializers.ActivateUsers()
    with pytest.raises(serializers.serializers.ValidationError):
        ser.validate_email('yo@micasa.com')


def test_ActivateUsers_validate_email_does_exist_is_active(mocker):
    get_user = mocker.patch.object(User.objects, 'get')
    mock_user = mocker.MagicMock(spec=User)
    mock_user.pwdtemporal = True
    mock_user.is_active = False
    get_user.return_value = mock_user
    ser = serializers.ActivateUsers()
    with pytest.raises(serializers.serializers.ValidationError):
        ser.validate_email('yo@micasa.com')


def test_ActivateUsers_validate_wisol(mocker):
    get_wisol_or_error = mocker.patch.object(serializers.ActivateUsers, 'get_wisol_or_error')
    mock_wisol = mocker.MagicMock(spec=Wisol)
    get_wisol_or_error.return_value = mock_wisol
    ser = serializers.ActivateUsers()
    control_serie = '4123'
    assert ser.validate_wisol(control_serie) == control_serie
    assert hasattr(ser, 'wisol') is True
    assert isinstance(ser.wisol, Wisol)
    get_wisol_or_error.assert_called_once_with(control_serie)


def test_ActivateUsers_clean_wisol_email_no_wisol(mocker):
    mock_wisol = mocker.MagicMock(spec=Wisol)
    mock_wisol.dispositivo.usuario.email = 'otro@bla.com'
    get_wisol_or_error = mocker.patch.object(serializers.ActivateUsers, 'get_wisol_or_error')
    get_wisol_or_error.return_value = mock_wisol
    ser = serializers.ActivateUsers()
    with pytest.raises(serializers.serializers.ValidationError):
        ser.clean_wisol_email({'serie': '41241', 'email': 'bla@com.com'})
    get_wisol_or_error.assert_called_once_with('41241')


@pytest.mark.django_db
def test_ActivateUsers_clean_wisol_email(mocker):
    dt = DeviceType.objects.create(key='bla', name='lnkasn')
    wisol = serializers.Wisol.objects.create(serie='41245', pac='kalks', deviceTypeId=dt)
    ser = serializers.ActivateUsers()
    error_message = 'Este chip no ha sido dado de alta correctamente'
    with pytest.raises(serializers.serializers.ValidationError) as err:
        ser.clean_wisol_email({'serie': wisol.serie, 'email': 'bla@com.com'})
    assert error_message in str(err.value)


def test_ActivateUsers_clean_wisol_email_with_wisol(mocker):
    mock_wisol = mocker.MagicMock(spec=Wisol)
    mock_wisol.dispositivo.usuario.email = 'otro@bla.com'
    get_wisol_or_error = mocker.patch.object(serializers.ActivateUsers, 'get_wisol_or_error')
    get_wisol_or_error.return_value = mock_wisol
    ser = serializers.ActivateUsers()
    ser.wisol = mock_wisol
    ser.clean_wisol_email({'serie': '41241', 'email': 'bla@com.com'})
    get_wisol_or_error.assert_not_called()


def test_ActivateUsers_clean_wisol_email_with_wisol_n_email(mocker):
    mock_wisol = mocker.MagicMock(spec=Wisol)
    mock_wisol.dispositivo.usuario.email = 'bla@com.com'
    get_wisol_or_error = mocker.patch.object(serializers.ActivateUsers, 'get_wisol_or_error')
    get_wisol_or_error.return_value = mock_wisol
    ser = serializers.ActivateUsers()
    ser.clean_wisol_email({'serie': '41241', 'email': 'bla@com.com'})
    get_wisol_or_error.assert_called_once_with('41241')


def test_ActivateUsers_clean_passwords():
    ser = serializers.ActivateUsers()
    attrs = {'password1': 'pwd3e4', 'password2': 'pwd3e4'}
    ser.clean_passwords(attrs)
    assert hasattr(ser, 'pwd') is True
    assert ser.pwd == 'pwd3e4'


def test_ActivateUsers_clean_passwords_error():
    ser = serializers.ActivateUsers()
    attrs = {'password1': 'pwd3e4', 'password2': 'pwdasdegt3e4'}
    with pytest.raises(serializers.serializers.ValidationError) as err:
        ser.clean_passwords(attrs)
    assert 'Los campos de password no coinciden.' in str(err.value)
    assert hasattr(ser, 'pwd') is False


def test_ActivateUsers_validate(mocker):
    clean_wisol_email = mocker.patch.object(serializers.ActivateUsers, 'clean_wisol_email')
    clean_passwords = mocker.patch.object(serializers.ActivateUsers, 'clean_passwords')
    ser = serializers.ActivateUsers()
    attrs = {'email': 'yo@hola.com', 'password1': 'pwd', 'password2': 'pwd'}
    ser.validate(attrs)
    clean_wisol_email.assert_called_once_with(attrs)
    clean_passwords.assert_called_once_with(attrs)


def test_ActivateUsers_save(mocker):
    usr = mocker.MagicMock(spec=User)
    set_password = mocker.MagicMock()
    usr.set_password = set_password
    save = mocker.MagicMock()
    usr.save = save
    usr.pwdtemporal = True
    usr.is_active = False
    ser = serializers.ActivateUsers()
    ser.pwd = 'password!!'
    ser.user = usr
    ser.save()
    set_password.assert_called_once_with('password!!')
    save.assert_called_once_with()


@pytest.mark.django_db
def test_Activate_users_integration_test_db():
    dt = DeviceType.objects.create(key='bla', name='lnkasn')
    wisol = serializers.Wisol.objects.create(serie='41245', pac='kalks', deviceTypeId=dt)
    control_user = User.objects.create_user(username='yo', email='yo@micorreo.com', pwdtemporal=True)
    data = {
        'wisol': wisol.serie,
        'email': control_user.email,
        'password1': 'pass1#@',
        'password2': 'pass1#@'
    }
    ser = serializers.ActivateUsers(data=data)
    assert ser.is_valid() is True, ser.errors
    usr = ser.save()
    assert isinstance(usr, User) is True
    assert usr.is_active is True
    assert usr.pwdtemporal is False
    assert isinstance(usr.pk, int) is True
