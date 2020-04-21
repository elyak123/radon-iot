from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from dj_rest_auth.serializers import JWTSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                           get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from radon.iot.serializers import NestedDispositivoSerializer
from radon.iot.models import Wisol, Dispositivo

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


class AsistedUserDispositivoCreation(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    wisol = serializers.CharField(required=True)
    location = GeometryField(precision=14)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_wisol(self, serie):
        try:
            self.wisol = Wisol.objects.get(serie=serie)
        except Wisol.DoesNotExist:
            raise serializers.ValidationError("El chip Wisol no existe o no ha sido registrado")
        if hasattr(self.wisol, 'dispositivo'):
            raise serializers.ValidationError("El chip Wisol ya tiene un dispositivo asignado")
        return serie

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'wisol': self.validated_data.get('wisol', ''),
            'location': self.validated_data.get('location', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        Dispositivo.objects.create(wisol=self.wisol, location=self.cleaned_data['location'], usuario=user)
        return user
