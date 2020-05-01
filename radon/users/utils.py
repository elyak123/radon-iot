from django.conf import settings
from django.contrib.auth import get_user_model


def get_default_user():
    return get_user_model().objects.get_or_create(username=settings.DEFAULT_USERNAME)[0].pk


def get_default_gasera():
    from radon.users.models import Gasera
    return Gasera.objects.get_or_create(nombre=settings.DEFAULT_GASERA)[0].pk


def create_user_and_dispositivo(user_data, disp_data):
    from radon.iot.models import Dispositivo
    user = get_user_model().objects.create_user(**user_data)
    user.save()
    disp_data['usuario'] = user
    disp = Dispositivo.objects.create(**disp_data)
    return user, disp
