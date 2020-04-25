from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from radon.iot import models

User = get_user_model()


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceType
        fields = ['pk', 'key', 'name']


class WisolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wisol
        fields = ['pk', 'serie', 'pac', 'deviceTypeId', 'prototype', ]


class DispositivoSerializer(GeoFeatureModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    # buscar limitar los querysets o revisar la implicacion de querysets abiertos.
    wisol = serializers.SlugRelatedField(queryset=models.Wisol.objects.all(), slug_field='serie')
    ultima_lectura = serializers.IntegerField(source='get_ultima_lectura', read_only=True)

    class Meta:
        model = models.Dispositivo
        geo_field = 'location'
        fields = ['wisol', 'capacidad', 'usuario', 'ultima_lectura']
        depth = 2


class NestedDispositivoSerializer(DispositivoSerializer):

    class Meta:
        model = models.Dispositivo
        geo_field = 'location'
        fields = ['pk', 'wisol', 'capacidad', 'ultima_lectura']
        depth = 2


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lectura
        fields = ['pk', 'fecha', 'nivel', 'dispositivo']


class InstalacionSerializer(serializers.ModelSerializer):
    operario = serializers.SlugRelatedField(queryset=models.User.objects.filter(tipo='OPERARIO'), slug_field='username')
    consumidor = serializers.SlugRelatedField(queryset=models.User.objects.filter(tipo='CONSUMIDOR'), slug_field='username')
    fecha = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Instalacion
        fields = ['fecha', 'operario', 'consumidor']
