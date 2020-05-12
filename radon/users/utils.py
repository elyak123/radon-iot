from django.conf import settings
from django.db.utils import ProgrammingError
from django.contrib.auth import get_user_model


def get_default_user():
    User = get_user_model()
    return User.objects.get_or_create(username=settings.DEFAULT_USERNAME)[0].pk


def get_default_gasera():
    from radon.users.models import Gasera
    try:
        return Gasera.objects.get_or_create(nombre=settings.DEFAULT_GASERA)[0].pk
    except ProgrammingError:
        return 1


def create_user_and_dispositivo(user_data, disp_data):
    from radon.iot.models import Dispositivo
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    user.save()
    disp_data['usuario'] = user
    disp = Dispositivo.objects.create(**disp_data)
    return user, disp
