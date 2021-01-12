from django.contrib.gis.geos import Polygon, MultiPolygon
from faker import Faker
import factory
import factory.fuzzy
from factory import random

fake = Faker(['es_MX'])


class FuzzyPolygon(factory.fuzzy.BaseFuzzyAttribute):
    """Yields random polygon"""
    tipo_mapping = {
        'localidad': {'lon_x': 0.07, 'lat_y': 0.05},
        'municipio': {'lon_x': 0.12, 'lat_y': 0.10}
    }

    def __init__(self, tipo, centroid=None, length=None, **kwargs):
        self.centroid = centroid
        self.type = tipo
        if length is None:
            length = random.randgen.randrange(3, 20, 1)
        if length < 3:
            raise Exception("Polygon needs to be 3 or greater in length.")
        self.length = length
        super().__init__(**kwargs)

    def get_centroid(self):
        if not self.centroid:
            return fake.local_latlng(country_code='MX', coords_only=True)
        return self.centroid

    def get_random_coords(self):
        centroid = self.get_centroid()
        return (
            fake.coordinate(center=centroid[0], radius=self.tipo_mapping[self.type]['lon_x']),
            fake.coordinate(center=centroid[1], radius=self.tipo_mapping[self.type]['lat_y'])
        )

    def fuzz(self):
        prefix = suffix = self.get_random_coords()
        coords = [self.get_random_coords() for __ in range(self.length - 1)]
        return Polygon([prefix] + coords + [suffix])


class FuzzyMultiPolygon(FuzzyPolygon):
    """Yields random multipolygon"""

    def fuzz(self):
        polygons = [super(FuzzyMultiPolygon, self).fuzz() for __ in range(self.length)]
        return MultiPolygon(*polygons)
