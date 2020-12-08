from rest_framework import serializers
from radon.georadon.models import Municipio, Localidad
from radon.market import models


class GaseraSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gasera
        fields = ['nombre']


class SucursalSerializer(serializers.ModelSerializer):
    gasera = serializers.SlugRelatedField(slug_field='nombre', queryset=models.Gasera.objects.all())
    municipio = serializers.SlugRelatedField(slug_field='nombre', queryset=Municipio.objects.all())
    localidad = serializers.SlugRelatedField(slug_field='clave', queryset=Localidad.objects.all())

    class Meta:
        model = models.Sucursal
        geo_field = 'ubicacion'
        fields = ['nombre', 'numeroPermiso', 'gasera', 'municipio', 'localidad', 'telefono']


class PrecioSerializer(serializers.ModelSerializer):
    sucursal = serializers.SlugRelatedField(slug_field='numeroPermiso', queryset=models.Precio.objects.all())

    class Meta:
        model = models.Precio
        fields = ['precio', 'fecha', 'sucursal']
