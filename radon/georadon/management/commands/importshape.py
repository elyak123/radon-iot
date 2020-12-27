from django.core.management.base import BaseCommand
from radon.georadon.utils import import_shape, get_path_for_shape


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('municipios', type=str, help='Nombre del shapefile de los municipios sin extensión.')
        parser.add_argument('localidades', type=str, help='Nombre del shapefile de las localidades sin extensión')

    def handle(self, *args, **kwargs):
        # Asumimos que el archivo deberia de estar en /data/muni_2018gw.shp
        import_shape(kwargs['municipios'], kwargs['localidades'])
        self.stdout.write(self.style.SUCCESS('Creados los municipios'))
