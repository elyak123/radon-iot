from rest_framework import viewsets, permissions
from radon.market import serializers


class GaseraViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GaseraSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'nombre'


class SucursalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SucursalSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'numeroPermiso'


class PrecioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PrecioSerializer
    permission_classes = [permissions.IsAdminUser]
