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

    def create(self, validated_data):
        clave = validated_data.pop('clave')
        localidad = models.Localidad.objects.get(clave=clave)
        qs = models.Sucursal.objects.filter(
            localidad__clave=clave
        ).select_related('gasera').values_list('numeroPermiso', 'gasera__nombre')
        sucursales = set([gas['sucursal']['numeroPermiso'] for gas in validated_data['data']])
        numeros_permiso = set([x[0] for x in qs])
        precios = []
        suc_existentes = sucursales.intersection(numeros_permiso)
        suc_por_crear = sucursales.difference(numeros_permiso)
        for per in suc_existentes:
            suc = models.Sucursal.objects.get(numeroPermiso=per)
            importe = list(map(
                    lambda x, per=per: x['sucursal']['precio'] if x['sucursal']['numeroPermiso'] == per else None,
                    validated_data['data']
                ))[0]
            importe = list(filter(
                    lambda x: x is not None,
                    list(map(
                        lambda x, per=per: x['sucursal']['precio'] if x['sucursal']['numeroPermiso'] == per else None,
                        validated_data['data']
                    ))))[0]
            precio = models.Precio(sucursal=suc, precio=importe)
            precios.append(precio)
        for no_creada in suc_por_crear:
            nombre_gasera = list(
                filter(
                    lambda x: x is not None, list(map(
                        lambda x, no_creada=no_creada: x['nombre'] if x['sucursal']['numeroPermiso'] == no_creada else None,
                        validated_data['data']))))[0]
            gasera, gasera_creada = models.Gasera.objects.get_or_create(nombre=nombre_gasera)
            nueva_sucursal = models.Sucursal.objects.create(
                numeroPermiso=no_creada, gasera=gasera, municipio=localidad.municipio)
            nueva_sucursal.localidad.add(localidad)
            importe = list(filter(
                lambda x: x is not None,
                list(map(
                    lambda x, no_creada=no_creada: x['sucursal']['precio'] if x['sucursal']['numeroPermiso'] == no_creada else None,
                    validated_data['data']))))[0]
            precio = models.Precio(sucursal=nueva_sucursal, precio=importe)
            precios.append(precio)
        models.Precio.objects.bulk_create(precios)
        return localidad

    def to_representation(self, instance):
        return {'sucess': True}  # por lo pronto.....
