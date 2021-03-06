"""
Production settings for Construbot project.

- Use WhiteNoise for serving static files
- Use Amazon's S3 for storing uploaded media
- Use mailgun to send emails
- Use Redis for cache

- Use sentry for error logging


"""


import logging
# import importlib

from .base import *  # noqa
import re
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')
DJANGO_DEFAULT_SUPERUSER_EMAIL = env('DJANGO_DEFAULT_SUPERUSER_EMAIL')
DJANGO_DEFAULT_SUPERUSER_USERNAME = env('DJANGO_DEFAULT_SUPERUSER_USERNAME')

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.io/
WHITENOISE_MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ]
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE.append('django_hosts.middleware.HostsResponseMiddleware')
WHITENOISE_MAX_AGE = 315360000
WHITENOISE_ALLOW_ALL_ORIGINS = True
WHITENOISE_KEEP_ONLY_HASHED_FILES = False  # si queremos True jsqrscanner necesita estar en S3


def immutable_file_test(path, url):
    # Match filename with 12 hex digits before the extension
    # e.g. app.db8f2edc0c8a.js
    return re.match(r'^.+[0-9a-f]{12}\..+$', url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test

# This SHA256 is for delete the address bar of the app.
PLAYSTORE_APP_KEY = env('PLAYSTORE_APP_KEY')


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_PRELOAD = 518400
SECURE_HSTS_SECONDS = 518400
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
SESSION_COOKIE_HTTPONLY = env.bool('SESSION_COOKIE_HTTPONLY', default=True)
SESSION_COOKIE_AGE = 31104000
ACCOUNT_SESSION_REMEMBER = True
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
CSRF_COOKIE_HTTPONLY = env.bool('CSRF_COOKIE_HTTPONLY', default=True)
X_FRAME_OPTIONS = 'SAMEORIGIN'

#INSTALLED_APPS += ['mod_wsgi.server', ]


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', 'drf_spectacular', ]

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

SNS_SIGFOX_ARN = env('SNS_SIGFOX_ARN')

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={AWS_EXPIRY}, s-maxage={AWS_EXPIRY}, must-revalidate"
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Static Assets
# ------------------------
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# COMPRESSOR
# ------------------------------------------------------------------------------
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)
COMPRESS_OFFLINE = env.bool('COMPRESS_OFFLINE', default=True)
COMPRESS_URL = STATIC_URL
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.rCSSMinFilter']
# HOSTS
# ---------------------
ROOT_HOSTCONF = 'radon.config.hosts'

# # EMAIL
# # ------------------------------------------------------------------------------
# DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
#                          default='Construbot <noreply@construbot.org>')
# EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Construbot]')
# SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# # Anymail with Mailgun
# INSTALLED_APPS += ['anymail', ]
# ANYMAIL = {
#     'MAILGUN_API_KEY': env('DJANGO_MAILGUN_API_KEY'),
#     'MAILGUN_SENDER_DOMAIN': env('MAILGUN_SENDER_DOMAIN')
# }
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# Use the Heroku-style specification
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db('DATABASE_URL', engine='django.contrib.gis.db.backends.postgis')
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)

# # CACHING
# # ------------------------------------------------------------------------------

# REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0)
# # Heroku URL does not pass the DB number, so we parse it in
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_LOCATION,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
#                                         # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#         }
#     }
# }

# Sentry Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        # Errors logged by the SDK itself
        'sentry_sdk': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
# # Sentry Configuration
SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_LOG_LEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send no events from log messages
)
sentry_sdk.init(
    SENTRY_DSN,
    integrations=[sentry_logging, DjangoIntegration()],
    send_default_pii=True
)

# # Custom Admin URL, use {% url 'admin:index' %}
# ADMIN_URL = env('DJANGO_ADMIN_URL')

# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
