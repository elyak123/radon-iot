from rest_framework.response import Response
from radon.georadon import serializers
from radon.iot.models import Localidad


def localidades_dispositivos(request):
    qs = Localidad.objects.filter(dispositivo__isnull=False).distinct()
    ser = serializers.LocalidadSerializer(qs, many=True)
    return Response(ser.data)
