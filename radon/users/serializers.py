from django.contrib.auth import get_user_model
from rest_framework import serializers
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
