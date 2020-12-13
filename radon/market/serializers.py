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
    localidad = serializers.SlugRelatedField(slug_field='clave', queryset=Localidad.objects.all(), many=True)

    class Meta:
        model = models.Sucursal
        geo_field = 'ubicacion'
        fields = ['gasera', 'numeroPermiso', 'municipio', 'localidad']


class PrecioSerializer(serializers.ModelSerializer):
    sucursal = SucursalSerializer()

    def create(self, validated_data):
        sucursal_data = validated_data.pop('sucursal')
        gasera , gasera_creada = models.Gasera.objects.get_or_create(nombre=sucursal_data['gasera']['nombre'])
        sucursal, sucursal_creada = models.Sucursal.objects.get_or_create(
            gasera=gasera,
            municipio=sucursal_data['municipio'],
            numeroPermiso=sucursal_data['numeroPermiso']
        )
        if sucursal_creada:
            for loc in sucursal_data['localidad']:
                sucursal.localidad.add(loc)
        precio = models.Precio.objects.create(precio=validated_data['precio'], sucursal=sucursal)
        return precio

    class Meta:
        model = models.Precio
        fields = ['precio', 'sucursal']
        depth = 3

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
