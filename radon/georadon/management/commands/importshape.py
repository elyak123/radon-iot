import errno
import os
from pathlib import Path
from collections import OrderedDict
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from radon.georadon.models import Estado, Municipio, Localidad


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('municipios', type=str, help='Nombre del shapefile de los municipios sin extensión.')
        parser.add_argument('localidades', type=str, help='Nombre del shapefile de las localidades sin extensión')

    def get_path(self, shapefile):
        local_shape = os.path.abspath(os.path.join(f'docker/production/django/data/{shapefile}.shp'))
        production_shape = os.path.abspath(os.path.join(f'/data/{shapefile}.shp'))
        if Path(local_shape).exists():
            return local_shape
        elif Path(production_shape).exists():
            return production_shape
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), shapefile)

    def handle(self, *args, **kwargs):
        # Asumimos que el archivo deberia de estar en /data/muni_2018gw.shp
        municipios_shape = self.get_path(kwargs['municipios'])
        mapping = {
            'estado': {'nombre': 'NOM_ENT'},
            'nombre': 'NOM_MUN',
            'clave': 'CVEGEO',
            'geo': 'MULTIPOLYGON'
        }
        ds = DataSource(str(municipios_shape))
        # Asumimos que solo es un layer
        layer = ds[0]
        estados = OrderedDict({feat.get('CVE_ENT'): feat.get('NOM_ENT') for feat in layer})
        Estado.objects.bulk_create([Estado(nombre=x[1]) for x in estados.items()])
        lm = LayerMapping(Municipio, municipios_shape, mapping, transform=False)
        lm.save(strict=True, verbose=True)

        localidades_shape = self.get_path(kwargs['localidades'])
        mapping_locals = {
            'nombre': 'NOMBRE',
            'clave': 'cve_mod',
            'municipio': {'nombre': 'Municipio'},
            'geo': 'POLYGON'
        }
        loc_ds =  DataSource(str(localidades_shape))
        lyr = loc_ds[0]
        lyr_mapping = LayerMapping(Localidad, localidades_shape, mapping_locals, transform=False)
        self.stdout.write(self.style.SUCCESS('Creados los municipios'))
