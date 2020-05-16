
def test_url_reverse_activacion_usuarios(tp):
    expected_url = '/users/activacion-usuarios/'
    reversed_url = tp.reverse('users:activacion-usuarios')
    assert expected_url == reversed_url


def test_url_reverse_user_dispositivo_registration(tp):
    expected_url = '/users/user-dispositivo-registration/'
    reversed_url = tp.reverse('users:usr-disp-reg')
    assert expected_url == reversed_url
