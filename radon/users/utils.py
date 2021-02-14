from django.conf import settings
from django.db.utils import ProgrammingError
from rest_framework.serializers import ValidationError
from xkcdpass import xkcd_password as xp
from unidecode import unidecode
from radon.georadon.models import Localidad
from radon.users.models import User


def get_default_user():
    try:
        usr = User.objects.raw("""
            SELECT id FROM users_user WHERE username = %(usrname)s ORDER BY id ASC LIMIT 1;
            """, params={'usrname': settings.DEFAULT_USERNAME})
        return usr[0].id
    except IndexError:
        pass


def get_default_gasera():
    from radon.users.models import Gasera
    try:
        return Gasera.objects.get_or_create(nombre=settings.DEFAULT_GASERA)[0].pk
    except ProgrammingError:
        return 1


def create_user_password(numwords=2):
    wordfile = xp.locate_wordfile('spa-mich')
    word_list = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)
    pwd = unidecode(xp.generate_xkcdpassword(word_list, numwords=numwords, delimiter='_'))
    return pwd


def get_localidad_from_wkt(point):
    try:
        loc = Localidad.objects.filter(geo__intersects=point).first()
        if loc is None:
            raise ValidationError('La Localidad no se encuentra en la base de datos.')
    except ValueError:
        raise ValidationError('La localidad o municipio se encuentra vacía')
    return loc


def create_user_and_dispositivo(user_data, disp_data):
    from radon.iot.models import Dispositivo
    user = User.objects.create_user(**user_data)
    user.save()
    disp_data['usuario'] = user
    disp = Dispositivo.objects.create(**disp_data)
    return user, disp
