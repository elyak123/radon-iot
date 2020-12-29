import errno
import os
from pathlib import Path
from collections import OrderedDict
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from radon.georadon.models import Estado, Municipio, Localidad


def get_path_for_shape(shapefile):
    local_shape = os.path.abspath(os.path.join(f'docker/production/django/data/{shapefile}.shp'))
    production_shape = os.path.abspath(os.path.join(f'/data/{shapefile}.shp'))
    if Path(local_shape).exists():
        return local_shape
    elif Path(production_shape).exists():
        return production_shape
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), shapefile)


def import_shapes(municipios, localidades):
    municipios_shape = get_path_for_shape(municipios)
    ds = DataSource(str(municipios_shape))
    layer = ds[0]
    estados = OrderedDict({feat.get('CVE_ENT'): feat.get('NOM_ENT') for feat in layer})
    Estado.objects.bulk_create([Estado(nombre=x[1]) for x in estados.items()])
    import_municipios(municipios)
    import_localidades(localidades)


def import_municipios(municipios):
    municipios_shape = get_path_for_shape(municipios)
    mapping = {
        'estado': {'nombre': 'NOM_ENT'},
        'nombre': 'NOM_MUN',
        'clave': 'CVEGEO',
        'geo': 'MULTIPOLYGON'
    }
    lm = LayerMapping(Municipio, municipios_shape, mapping, transform=False)
    lm.save(strict=True, verbose=True)


def import_localidades(localidades):
    localidades_shape = get_path_for_shape(localidades)
    mapping_locals = {
        'nombre': 'NOMBRE',
        'clave': 'cve_mod',
        'municipio': {'nombre': 'Municipio'},
        'geo': 'MULTIPOLYGON'
    }
    lyr_mapping = LayerMapping(Localidad, localidades_shape, mapping_locals, transform=False)
    lyr_mapping.save(strict=True, verbose=True)


def create_estado(estado):
    return Estado.objects.create(nombre=estado)
