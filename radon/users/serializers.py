from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.serializers import JWTSerializer
from radon.iot.serializers import NestedDispositivoSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    dispositivo_set = NestedDispositivoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'dispositivo_set'
        ]
        depth = 2


class ExpirationJWTSerializer(JWTSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_access_token(self, obj):
        return {'access': str(obj['access_token']), 'exp': obj['access_token']['exp']}

    def get_refresh_token(self, obj):
        return {"refresh_token":  str(obj['refresh_token']), 'exp': obj['refresh_token']['exp']}
