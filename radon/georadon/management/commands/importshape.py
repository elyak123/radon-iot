import os
from pathlib import Path
from collections import OrderedDict
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from radon.georadon.models import Estado, Municipio


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Asumimos que el archivo deberia de estar en /data/muni_2018gw.shp
        local_shape = os.path.abspath(os.path.join('docker/production/django/data/muni_2018gw.shp'))
        production_shape = os.path.abspath(os.path.join('/data/muni_2018gw.shp'))
        Estado.objects.all().delete()
        Municipio.objects.all().delete()
        if Path(local_shape).exists():
            shape = local_shape
        elif Path(production_shape).exists():
            shape = production_shape
        mapping = {
            'estado': {'nombre': 'NOM_ENT'},
            'nombre': 'NOM_MUN',
            'clave': 'CVEGEO',
            'geo': 'MULTIPOLYGON'
        }
        ds = DataSource(str(shape))
        # Asumimos que solo es un layer
        layer = ds[0]
        estados = OrderedDict({feat.get('CVE_ENT'): feat.get('NOM_ENT') for feat in layer})
        Estado.objects.bulk_create([Estado(nombre=x[1]) for x in estados.items()])
        lm = LayerMapping(Municipio, shape, mapping, transform=False)
        lm.save(strict=True, verbose=True)
        self.stdout.write(self.style.SUCCESS('Creados los municipios'))
        if not Path(local_shape).exists() and not Path(production_shape).exists():
            self.stdout.write('No hay municipios que crear')
