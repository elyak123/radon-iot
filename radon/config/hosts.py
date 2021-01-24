from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'soporte', settings.ROOT_URLCONF, name='soporte'),
    host(r'app', 'radon.app.urls', name='app'),
    host(r'operador', 'radon.operador.urls', name='operador'),
    host(r'api', 'radon.api.urls.urls', name='api'),
    host(r'crm', 'radon.crm.urls', name='crm'),
    host(r'rutas', 'radon.rutas.urls', name='rutas'),
    host(r'www', 'radon.www.urls', name='www'),
)
