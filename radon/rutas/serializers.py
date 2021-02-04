from rest_framework import serializers
from radon.market.models import Gasera
from radon.rutas import models


class PedidoSerialiser(serializers.ModelSerializer):
    gasera = serializers.CharField()

    class Meta:
        model = models.Pedido
        fields = ['cantidad', 'dispositivo', 'precio', 'gasera']

    def validate(self, attrs):
        gasera = Gasera.objects.get(nombre=attrs['gasera'])
        if gasera == attrs['precio'].sucursal.gasera.nombre:
            raise serializers.ValidationError('La gasera no coincide con el precio.')
        return attrs
