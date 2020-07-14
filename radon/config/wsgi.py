"""
WSGI config for radon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import environ

from django.core.wsgi import get_wsgi_application

env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
WSGI_PATH = environ.Path(__file__)  # radon/radon/config/wsgi.py
ROOT_DIR = WSGI_PATH - 3  # radon/radon/config/wsgi.py -3 = radon/

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    env.read_env(env_file)
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        env('DJANGO_SETTINGS_MODULE')
    )
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "radon.config.settings.production"
    )

application = get_wsgi_application()
