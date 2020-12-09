from rest_framework import serializers
from radon.georadon.models import Municipio, Localidad
from radon.market import models


class GaseraSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gasera
        fields = ['nombre']


class SucursalSerializer(serializers.ModelSerializer):
    gasera = GaseraSerializer()
    municipio = serializers.SlugRelatedField(slug_field='clave', queryset=Municipio.objects.all())
    localidad = serializers.SlugRelatedField(slug_field='clave', queryset=Localidad.objects.all())

    class Meta:
        model = models.Sucursal
        geo_field = 'ubicacion'
        fields = ['gasera', 'numeroPermiso', 'municipio', 'localidad']


class PrecioSerializer(serializers.ModelSerializer):
    sucursal = SucursalSerializer(many=True)

    class Meta:
        model = models.Precio
        fields = ['precio', 'sucursal']


"""
[
    {
        "sucursal": {
            "gasera": {
                "nombre": "Empresa, S.A. de C.V."
            },
            "municipio": "01001",
            "localidad": "010012439",
            "numeroPermiso": "LP/0234/2019"
        },
        "precio": 12
    },
    {
        "sucursal": {
            "gasera": {
                "nombre": "Empresa, S.A. de C.V."
            },
            "municipio": "01001",
            "localidad": "010012439",
            "numeroPermiso": "LP/0234/2019"
        },
        "precio": 12
    },
    {
        "sucursal": {
            "gasera": {
                "nombre": "Empresa, S.A. de C.V."
            },
            "municipio": "01001",
            "localidad": "010012439",
            "numeroPermiso": "LP/0234/2019"
        },
        "precio": 12
    }
]
"""
