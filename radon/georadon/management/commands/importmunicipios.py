from django.core.management.base import BaseCommand
from radon.georadon.utils import import_municipios


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('municipios', type=str, help='Nombre del shapefile de las municipios sin extensión')

    def handle(self, *args, **kwargs):
        import_municipios(kwargs['municipios'])
        self.stdout.write(self.style.SUCCESS('Municipios Creadas'))
