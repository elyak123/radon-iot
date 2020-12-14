from rest_framework import serializers
from radon.market import models


class SucursalSerializer(serializers.Serializer):
    numeroPermiso = serializers.CharField()
    precio = serializers.DecimalField(max_digits=12, decimal_places=2)

    # class Meta:
    #     fields = ['numeroPermiso', 'precio']


class GaseraSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    sucursal = SucursalSerializer()

    # class Meta:
    #     fields = ['nombre', 'sucursal']


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


class PrecioSerializer(serializers.ModelSerializer):
    sucursal = SucursalSerializer()

    def create(self, validated_data):
        sucursal_data = validated_data.pop('sucursal')
        gasera, gasera_creada = models.Gasera.objects.get_or_create(nombre=sucursal_data['gasera']['nombre'])
        sucursal, sucursal_creada = models.Sucursal.objects.get_or_create(
            gasera=gasera,
            municipio=sucursal_data['municipio'],
            numeroPermiso=sucursal_data['numeroPermiso']
        )
        if sucursal_creada:
            for loc in sucursal_data['localidad']:
                sucursal.localidad.add(loc)
        precio = models.Precio.objects.create(precio=validated_data['precio'], sucursal=sucursal)
        return precio

    class Meta:
        model = models.Precio
        fields = ['precio', 'sucursal']
        depth = 3

"""
[
    {
        "sucursal": {
            "gasera": {
                "nombre": "Empresa, S.A. de C.V."
            },
            "municipio": "01001",
            "localidad": ["010012439"],
            "numeroPermiso": "LP/0234/2019"
        },
        "precio": 12
    },
    {
        "sucursal": {
            "gasera": {
                "nombre": "Empresa, S.A. de C.V."
            },
            "municipio": "01001",
            "localidad": "010012439",
            "numeroPermiso": "LP/0234/2019"
        },
        "precio": 12
    },
    {
        "sucursal": {
            "gasera": {
                "nombre": "Empresa, S.A. de C.V."
            },
            "municipio": "01001",
            "localidad": "010012439",
            "numeroPermiso": "LP/0234/2019"
        },
        "precio": 12
    }
]
"""
