from radon.users import utils
from radon.users.models import User
from radon.market.models import Sucursal
from radon.iot.models import Dispositivo, Wisol


def test_get_default_user_other(mocker, settings):
    settings.DEFAULT_USERNAME = 'foo'
    mock_usr = mocker.MagicMock()
    mock_pk = mocker.MagicMock(id=2)
    mock_usr.__getitem__.side_effect = lambda a: mock_pk
    attrs = {
        'objects.raw.return_value': mock_usr
    }
    mock_user_klass = mocker.MagicMock()
    mock_user_klass.configure_mock(**attrs)
    mocker.patch('radon.users.utils.User', mock_user_klass)
    assert utils.get_default_user() == 2
    mock_user_klass.objects.raw.assert_called_once_with("""
            SELECT id FROM users_user WHERE username = %(usrname)s ORDER BY id ASC LIMIT 1;
            """, params={'usrname': 'foo'})


def test_create_user_and_dispositivo(mocker):
    mocker.patch('radon.market.models.Gasera')
    usr = mocker.MagicMock(spec=User, pk=2)
    usr_save = mocker.MagicMock()
    usr.save = usr_save
    sucursal = mocker.MagicMock(spec=Sucursal, pk=1)
    attrs = {
        'objects.create_user.return_value': usr
    }
    user_data = {
        'username': 'my_username',
        'email': 'yo@email.com',
        'sucursal': sucursal,
        'tipo': 'CONSUMIDOR',
        'pwdtemporal': True,
    }
    disp_data = {
        'wisol': mocker.MagicMock(spec=Wisol),
        'location': 'POINT(122.33245 -123.56321)',
        'capacidad': 122
    }
    mock_user_klass = mocker.MagicMock(**attrs)
    mocker.patch('radon.users.utils.User', mock_user_klass)
    mock_disp = mocker.patch('radon.iot.models.Dispositivo')
    disp_instance = mocker.MagicMock(spec=Dispositivo, pk=4)
    disp_attrs = {'objects.create.return_value': disp_instance}
    mock_disp.configure_mock(**disp_attrs)
    user, dispositivo = utils.create_user_and_dispositivo(user_data, disp_data)
    assert isinstance(user, User) is True
    assert user.pk == 2
    assert dispositivo.pk == 4
    assert isinstance(dispositivo, Dispositivo) is True
    mock_disp.objects.create.assert_called_once_with(**disp_data)
    mock_user_klass.objects.create_user.assert_called_once_with(**user_data)
    usr_save.assert_called_once_with()
