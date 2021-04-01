from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from radon.rutas import serializers
from radon.rutas.models import Position, Pedido
from django.views.decorators.csrf import csrf_exempt


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PedidoSerialiser
    queryset = Pedido.objects.all()

    def get_queryset(self):
        try:
            if self.request.user.tipo == 'CONSUMIDOR':
                return Pedido.objects.filter(
                    dispositivo__wisol__serie=self.request.GET['dispositivo'],
                    dispositivo__usuario=self.request.user
                )
            elif self.request.user.tipo == 'STAFF':
                return Pedido.objects.filter(
                    dispositivo__wisol__serie=self.request.GET['dispositivo']
                )
        except KeyError:
            if self.request.user.tipo == 'CONSUMIDOR':
                return Pedido.objects.filter(dispositivo__usuario=self.request.user)
            elif self.request.user.tipo == 'STAFF':
                return Pedido.objects.all()
        return None
