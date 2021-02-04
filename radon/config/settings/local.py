import sys
from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
try:
    HOST_PORT = sys.argv[-1].split(':')[1]
except IndexError:  # En caso de que se corran otros commandos.
    HOST_PORT = ''

MOCK_URL_CONF = env('DJANGO_MOCK_URL_CONF', default='radon.app.urls')
# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env.int('DJANGO_SITE_ID', '')
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

MIDDLEWARE.append('django_hosts.middleware.HostsResponseMiddleware')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='-r&khdeo$%xzj!o_xj@4ry=u7$urt(n@m8u@1ive#r46i@i5cs')
TEST_USERNAME = env('TEST_USERNAME', default='')
TEST_PASSWORD = env('TEST_PASSWORD', default='')
TEST_URL = env('TEST_URL', default='')
