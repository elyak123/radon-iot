from rest_framework import serializers
from radon.georadon import models


class LocalidadSerializer(serializers.ModelSerializer):
    descompuesto = serializers.CharField(source='descompuesto', read_only=True)

    class Meta:
        model = models.Localidad
        geo_field = 'geo'
        fields = ['descompuesto']
