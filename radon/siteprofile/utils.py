from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
from radon.siteprofile.models import Sitio


def create_sites():
    for host in settings.ALLOWED_HOSTS:
        name = host.split('.')[0]
        if f'radon.{name}.apps.{name[0].upper()}{name[1:]}Config' in settings.INSTALLED_APPS:
            Sitio.objects.get_or_create(
                domain=host,
                name=name,
                modulo='radon.'+name+'.urls'
            )
        else:
            raise ImproperlyConfigured(f'¡La app {name} no existe en el proyecto!')
        try:
            example = Site.objects.get(domain='example.com')
            example.delete()
        except Site.DoesNotExist:
            pass
