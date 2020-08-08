from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from radon.iot import models

User = get_user_model()


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceType
        fields = ['pk', 'key', 'name']


class WisolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wisol
        fields = ['pk', 'serie', 'pac', 'deviceTypeId', 'prototype', ]


class WisolValidation(serializers.Serializer):
    """
    ENDPOINT:
    /iot/disponibilidad-wisol/
    POST
    wisol: <serie>

    VALIDA:
    * Wisol con serie existe
    * Wisol disponible (sin dispositivo o Usuario)
    """
    wisol = serializers.CharField(required=True)
    not_wisol_error = 'El chip que corresponde al dispositivo no existe favor de llamar a soporte.'

    def get_wisol_or_error(self, serie):
        try:
            wisol = models.Wisol.objects.get(serie=serie)
        except models.Wisol.DoesNotExist:
            raise serializers.ValidationError(self.not_wisol_error)
        return wisol

    def validate_wisol(self, serie):
        self.wisol = self.get_wisol_or_error(serie)
        if self.wisol.activo:
            raise serializers.ValidationError("El chip Wisol ya tiene un dispositivo asignado")
        return serie


class DispositivoSerializer(GeoFeatureModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # buscar limitar los querysets o revisar la implicacion de querysets abiertos.
    wisol = serializers.SlugRelatedField(queryset=models.Wisol.objects.all(), slug_field='serie')
    ultima_lectura = serializers.IntegerField(source='get_ultima_lectura', read_only=True)

    class Meta:
        model = models.Dispositivo
        geo_field = 'location'
        fields = ['wisol', 'capacidad', 'usuario', 'ultima_lectura']
        depth = 2


class NestedDispositivoSerializer(DispositivoSerializer):

    class Meta:
        model = models.Dispositivo
        geo_field = 'location'
        fields = ['pk', 'wisol', 'capacidad', 'ultima_lectura']
        depth = 2


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lectura
        fields = ['pk', 'fecha', 'nivel', 'dispositivo']


class InstalacionSerializer(serializers.ModelSerializer):
    operario = serializers.SlugRelatedField(queryset=User.objects.filter(tipo='OPERARIO'), slug_field='username')
    consumidor = serializers.SlugRelatedField(queryset=User.objects.filter(tipo='CONSUMIDOR'), slug_field='username')
    fecha = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Instalacion
        fields = ['fecha', 'operario', 'consumidor', 'folio']
