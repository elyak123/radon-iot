from django.conf import settings
from django.contrib.auth import get_user_model


def get_default_user():
    return get_user_model().objects.get_or_create(username=settings.DEFAULT_USERNAME)[0].pk


def get_default_gasera():
    from radon.users.models import Gasera
    return Gasera.objects.get_or_create(nombre=settings.DEFAULT_GASERA)[0].pk
