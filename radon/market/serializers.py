from rest_framework import serializers
from radon.market import models


class SucursalSerializer(serializers.Serializer):
    numeroPermiso = serializers.CharField()
    precio = serializers.DecimalField(max_digits=12, decimal_places=2)


class GaseraSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    sucursal = SucursalSerializer()


class MarketLocalidadSerializer(serializers.Serializer):
    clave = serializers.CharField()
    data = GaseraSerializer(many=True)

    def importe_sucursal(self, data, permiso):
        return self.dynamic_mapping(data, self.mapping_wrapper(permiso, 'precio'))

    def nombre_gasera(self, data, permiso):
        return self.dynamic_mapping(data, self.mapping_wrapper(permiso, 'nombre'))

    def lambda_return_value(self, x, attr):
        if attr == 'nombre':
            return x['nombre']
        return x['sucursal']['precio']

    def mapping_wrapper(self, numero_permiso, attr):
        return (lambda x, permiso=numero_permiso:
                self.lambda_return_value(x, attr) if x['sucursal']['numeroPermiso'] == permiso else None)

    def dynamic_mapping(self, data, func):
        return list(filter(lambda x: x is not None, list(map(func, data))))[0]

    def get_sucursal(self, data, permiso):
        try:
            suc = models.Sucursal.objects.get(numeroPermiso=permiso)
        except models.Sucursal.DoesNotExist:
            nombre_gasera = self.nombre_gasera(data, permiso)
            gasera, gasera_creada = models.Gasera.objects.get_or_create(nombre__iexact=nombre_gasera)
            suc = models.Sucursal.objects.create(
                numeroPermiso=permiso,
                gasera=gasera
            )
        return suc

    def procesar_sucursal(self, data, permiso, localidad):
        importe = self.importe_sucursal(data, permiso)
        suc = self.get_sucursal(data, permiso)
        precio = models.Precio(sucursal=suc, precio=importe, localidad=localidad)
        return precio

    def create(self, validated_data):
        clave = validated_data.pop('clave')
        localidad = models.Localidad.objects.get(clave=clave)
        precios = []
        permisos = set([gas['sucursal']['numeroPermiso'] for gas in validated_data['data']])
        for perm in permisos:
            precio = self.procesar_sucursal(validated_data['data'], perm, localidad)
            precios.append(precio)
        models.Precio.objects.bulk_create(precios)
        return localidad

    def to_representation(self, instance):
        return {'sucess': True}  # por lo pronto.....
