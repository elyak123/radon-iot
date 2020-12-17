from rest_framework import serializers
from radon.rutas import models


class PedidoSerialiser(serializers.ModelSerializer):
    gasera = serializers.SlugRelatedField(slug_field='precio__sucursal__gasera__nombre')

    class Meta:
        model = models.Pedido
        fields = ['cantidad', 'dispositivo', 'precio', 'gasera']

    def validate(self, attrs):
        pass
        #gasera = 
