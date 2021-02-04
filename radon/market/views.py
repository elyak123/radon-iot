from rest_framework import viewsets
from radon.market import serializers, models


class GaseraViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GaseraSerializer
    queryset = models.Gasera.objects.all()
    lookup_field = 'nombre'


class SucursalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SucursalSerializer
    queryset = models.Sucursal.objects.all()
    lookup_field = 'numeroPermiso'


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
