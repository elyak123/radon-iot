from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from radon.rutas import serializers
from radon.rutas.models import Position, Pedido
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def endpointgps(request):
    if request.method == 'GET':
        get = request.GET
        pos = Position.objects.create(location=f'POINT({get["lat"]} {get["lon"]})')
    elif request.method == 'POST':
        post = request.POST
        pos = Position.objects.create(location=f'POINT({post["lat"]} {post["lon"]})')
        return JsonResponse({'metodo': 'POST', 'contenido': 'Hola desde POST', 'pos': pos.location})


def last_pos(request):
    pos = Position.objects.all().order_by('-fecha_creacion').first()
    if pos:
        return JsonResponse({'lat': pos.location.x, 'lon': pos.location.y})
    return JsonResponse({'disps': 'todavia no tienes dispositivos'})


def mapa(request):
    return render(request, 'rutas/gps_display.html')


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PedidoSerialiser
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pedido.objects.all()
