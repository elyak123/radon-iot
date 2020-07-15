import os

os.environ['DJANGO_SETTINGS_MODULE'] = ''
os.environ['DATABASE_URL'] = ''
os.environ['DJANGO_ALLOWED_HOSTS'] = ''
os.environ['DOMAIN_NAME'] = ''
os.environ['DJANGO_SECRET_KEY'] = ''
os.environ['SIMPLE_JWT_SIGNING_KEY'] = ''
os.environ['DEFAULT_USERNAME'] = ''
os.environ['DEFAULT_GASERA'] = ''
os.environ['GOOGLE_MAPS_API_KEY'] = ''
os.environ['TEST_URL'] = ''
os.environ['TEST_USERNAME'] = ''
os.environ['TEST_PASSWORD'] = ''
os.environ['DJANGO_AWS_STORAGE_BUCKET_NAME'] = ''
os.environ['DJANGO_AWS_ACCESS_KEY_ID'] = ''
os.environ['DJANGO_AWS_SECRET_ACCESS_KEY'] = ''

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
