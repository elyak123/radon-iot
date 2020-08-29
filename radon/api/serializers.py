from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.serializers import JWTSerializer


class ExpirationJWTSerializer(JWTSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_access_token(self, obj):
        return {'token': str(obj['access_token']), 'exp': obj['access_token']['exp']}

    def get_refresh_token(self, obj):
        return {"token":  str(obj['refresh_token']), 'exp': obj['refresh_token']['exp']}


class ExpirationRefreshJWTSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': {'token': str(refresh.access_token), 'exp': refresh.access_token['exp']}}
        if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
            if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass
            refresh.set_jti()
            refresh.set_exp()
            data['refresh'] = {'token': str(refresh), 'exp': refresh['exp']}
        else:
            data = {'refresh': {**data['access'], 'type': 'access'}}
        return data
