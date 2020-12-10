from rest_framework.response import Response
from radon.georadon import serializers


def localidades_dispositivos(request):
    ser = serializers.LocalidadSerializer(data=request.data, many=True)
    ser.is_valid(raise_exception=True)
    return Response(ser.data)
