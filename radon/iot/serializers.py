from rest_framework import serializers
from radon.iot import models


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceType
        fields = ['pk', 'key', 'name']


class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dispositivo
        fields = ['pk', 'serie', 'capacidad', 'deviceTypeId', 'pac', 'prototype']
