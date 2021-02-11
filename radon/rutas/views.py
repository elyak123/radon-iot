from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from radon.rutas import serializers
from radon.rutas.models import Position, Pedido
from django.views.decorators.csrf import csrf_exempt


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PedidoSerialiser
    queryset = Pedido.objects.all()
