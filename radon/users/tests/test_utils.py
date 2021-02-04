from radon.users import utils
from radon.users.models import User
from radon.market.models import Gasera
from radon.iot.models import Dispositivo, Wisol


def test_get_default_user_other(mocker, settings): # FALLA
    settings.DEFAULT_USERNAME = 'foo'
    attrs = {
        'objects.get_or_create.return_value': (mocker.MagicMock(spec=User, pk=2), True)
    }
    mock_user_klass = mocker.MagicMock(**attrs)
    mocker.patch('radon.users.utils.get_user_model', return_value=mock_user_klass)
    assert utils.get_default_user() == 2
    mock_user_klass.objects.get_or_create.assert_called_once_with(username='foo')


def test_create_user_and_dispositivo(mocker): # FALLA
    mocker.patch('radon.users.models.Gasera')
    usr = mocker.MagicMock(spec=User, pk=2)
    usr_save = mocker.MagicMock()
    usr.save = usr_save
    gasera = mocker.MagicMock(spec=Gasera, pk=1)
    attrs = {
        'objects.create_user.return_value': usr
    }
    user_data = {
        'username': 'my_username',
        'email': 'yo@email.com',
        'gasera': gasera,
        'tipo': 'CONSUMIDOR',
        'pwdtemporal': True,
    }
    disp_data = {
        'wisol': mocker.MagicMock(spec=Wisol),
        'location': 'POINT(122.33245 -123.56321)',
        'capacidad': 122
    }
    mock_user_klass = mocker.MagicMock(**attrs)
    usr_getter = mocker.patch('radon.users.utils.get_user_model', return_value=mock_user_klass)
    mock_disp = mocker.patch('radon.iot.models.Dispositivo')
    disp_instance = mocker.MagicMock(spec=Dispositivo, pk=4)
    disp_attrs = {'objects.create.return_value': disp_instance}
    mock_disp.configure_mock(**disp_attrs)
    user, dispositivo = utils.create_user_and_dispositivo(user_data, disp_data)
    usr_getter.assert_called_once_with()
    assert isinstance(user, User) is True
    assert user.pk == 2
    assert dispositivo.pk == 4
    assert isinstance(dispositivo, Dispositivo) is True
    mock_disp.objects.create.assert_called_once_with(**disp_data)
    mock_user_klass.objects.create_user.assert_called_once_with(**user_data)
    usr_save.assert_called_once_with()
