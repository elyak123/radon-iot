from rest_framework import serializers
from radon.georadon import models


class LocalidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Localidad
        geo_field = 'geo'
        fields = ['clave']
