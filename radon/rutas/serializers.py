from rest_framework import serializers
from django.db.models import Q
from radon.market.models import Precio
from radon.rutas import models
from radon.iot.models import Dispositivo
from radon.market.serializers import PrecioSerializer


class PedidoSerialiser(serializers.ModelSerializer):
    mensajes = serializers.StringRelatedField(many=True, required=False)
    precio = PrecioSerializer(read_only=True)
    dispositivo = serializers.CharField(source="dispositivo.wisol.serie")

    class Meta:
        model = models.Pedido
        fields = ['pk', 'cantidad', 'dispositivo', 'precio', 'mensajes']

    def validate(self, attrs):
        usuario = self.context['request'].user
        pedidos = models.Pedido.objects.filter(Q(estado='INICIADO') | Q(estado='EN PROCESO'),
                                               dispositivo__wisol__serie=attrs['dispositivo']['wisol']['serie'],
                                               dispositivo__usuario=usuario)
        if pedidos.exists():
            raise serializers.ValidationError('Ya existe un pedido en proceso para este dispositivo.')
        return attrs

    def create(self, validated_data):
        dispositivo = Dispositivo.objects.get(wisol__serie=self.initial_data['dispositivo'])
        precio = Precio.objects.get(pk=self.initial_data['precio'])
        return models.Pedido(precio=precio,
                             cantidad=self.initial_data['cantidad'],
                             dispositivo=dispositivo)
