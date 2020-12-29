from django.core.management.base import BaseCommand
from radon.georadon.utils import import_localidades


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('localidades', type=str, help='Nombre del shapefile de las localidades sin extensión')

    def handle(self, *args, **kwargs):
        # Asumimos que el archivo deberia de estar en /data/muni_2018gw.shp
        import_localidades(kwargs['localidades'])
        self.stdout.write(self.style.SUCCESS('Localidades Creadas'))
