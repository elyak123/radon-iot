from rest_framework import serializers
from radon.iot.models import Dispositivo


class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = ['serie', 'capacidad', 'deviceTypeId', 'pac', 'prototype']
