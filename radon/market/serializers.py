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
                self.lambda_return_value(attr) if x['sucursal']['numeroPermiso'] == permiso else None)

    def dynamic_mapping(self, data, func):
        return list(filter(lambda x: x is not None, list(map(func, data))))[0]

    def clasificar_sucursales(self, clave, data):
        qs = models.Sucursal.objects.filter(
            localidad__clave=clave
        ).select_related('gasera').values_list('numeroPermiso', 'gasera__nombre')
        sucursales = set([gas['sucursal']['numeroPermiso'] for gas in data])
        numeros_permiso = set([x[0] for x in qs])
        suc_existentes = sucursales.intersection(numeros_permiso)
        suc_por_crear = sucursales.difference(numeros_permiso)
        return suc_existentes, suc_por_crear

    def get_sucursal(self, data, permiso, existente, localidad):
        try:
            suc = models.Sucursal.objects.get(numeroPermiso=permiso)
        except models.Sucursal.DoesNotExist:
            nombre_gasera = self.nombre_gasera(data, permiso)
            gasera, gasera_creada = models.Gasera.objects.get_or_create(nombre=nombre_gasera)
            suc = models.Sucursal.objects.create(
                numeroPermiso=permiso,
                gasera=gasera,
                municipio=localidad.municipio
            )
        if not existente:
            suc.localidad.add(localidad)
        return suc

    def procesar_sucursal(self, data, permiso, existente, localidad):
        importe = self.importe_sucursal(data, permiso)
        suc = self.get_sucursal(data, permiso, existente, localidad)
        precio = models.Precio(sucursal=suc, precio=importe)
        return precio

    def create(self, validated_data):
        clave = validated_data.pop('clave')
        localidad = models.Localidad.objects.get(clave=clave)
        precios = []
        suc_existentes, suc_por_crear = self.clasificar_sucursales(clave, validated_data['data'])
        for per in suc_existentes:
            precio = self.procesar_sucursal(validated_data['data'], per, True, localidad)
            precios.append(precio)
        for no_creada in suc_por_crear:
            precio = self.procesar_sucursal(validated_data['data'], per, False, localidad)
            precios.append(precio)
        models.Precio.objects.bulk_create(precios)
        return localidad

    def to_representation(self, instance):
        return {'sucess': True}  # por lo pronto.....
