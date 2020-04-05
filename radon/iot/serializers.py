from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
# from phonenumber_field.serializerfields import PhoneNumberField
from radon.iot import models

User = get_user_model()


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceType
        fields = ['pk', 'key', 'name']


class DispositivoSerializer(GeoFeatureModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())
    deviceTypeId = serializers.PrimaryKeyRelatedField(queryset=models.DeviceType.objects.all())
    ultima_lectura = serializers.IntegerField(source='get_ultima_lectura', read_only=True)

    class Meta:
        model = models.Dispositivo
        geo_field = 'location'
        fields = ['pk', 'serie', 'capacidad', 'deviceTypeId', 'pac', 'prototype', 'usuario', 'ultima_lectura']
        depth = 2


class NestedDispositivoSerializer(DispositivoSerializer):

    class Meta:
        model = models.Dispositivo
        geo_field = 'location'
        fields = ['pk', 'serie', 'capacidad', 'deviceTypeId', 'pac', 'prototype', 'ultima_lectura']
        depth = 2


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lectura
        fields = ['pk', 'fecha', 'nivel', 'dispositivo']
