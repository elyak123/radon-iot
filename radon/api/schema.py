from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_basic_type
from drf_spectacular.types import OpenApiTypes


class UserClassificationJWTCookieAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'radon.api.auth.UserClassificationJWTCookieAuthentication'
    name = 'UserClassificationJWTCookieAuthentication'  # name used in the schema

    def get_security_definition(self, auto_schema):
        descripcion = 'Autenticación que soporta JWT en el Authentication header, así como mediante cookie,'
        'Autenticación mediante el header toma precedencia.'

        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': descripcion,
        }


class GeometryFieldFieldExtension(OpenApiSerializerFieldExtension):
    target_class = 'rest_framework_gis.fields.GeometryField'

    def map_serializer_field(self, auto_schema, direction):
        # equivalent to return {'type': 'dict'}
        return build_basic_type(OpenApiTypes.OBJECT)
