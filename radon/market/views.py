from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from radon.market import serializers, models
from radon.iot.models import Dispositivo


class GaseraViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GaseraSerializer
    queryset = models.Gasera.objects.all()
    lookup_field = 'nombre'


class SucursalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SucursalSerializer
    queryset = models.Sucursal.objects.all()
    lookup_field = 'numeroPermiso'


class ListSucursalesByDispositivoView(APIView):
    def get(self, request, wisol):
        try:
            localidad = Dispositivo.objects.get(wisol__serie=wisol, usuario=request.user).localidad
            sucursales = models.Sucursal.especial.from_localidad(localidad)
            for i in sucursales:
                precio = models.Sucursal.objects.get(pk=sucursales[0]['sucursal_pk']).precio_set.last()
                i['precio'] = precio.precio
            respuesta = [x for x in sucursales]
        except Dispositivo.DoesNotExist:
            respuesta = {
                'error': 'No hay sucursales para el dispositivo seleccionado.'
            }
            return Response(respuesta, 401)
        return Response(respuesta)


class PreciosViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MarketLocalidadSerializer
    queryset = models.Precio.objects.all()

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['many'] = True
        return serializer_class(*args, **kwargs)
