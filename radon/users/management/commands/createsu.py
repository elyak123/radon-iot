from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            su = User.objects.get(email=os.environ['DJANGO_DEFAULT_SUPERUSER_EMAIL'])
            if not su.is_superuser:
                raise ImproperlyConfigured('Default superuser exists but has no is_superuser = False')
        except User.DoesNotExist:
            User.objects.create_superuser(
                email=settings.DJANGO_DEFAULT_SUPERUSER_EMAIL,
                username=settings.DJANGO_DEFAULT_SUPERUSER_USERNAME,
                tipo='STAFF',
                password=settings.DJANGO_DEFAULT_SUPERUSER_PASSWORD
            )
