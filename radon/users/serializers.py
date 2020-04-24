from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.serializers import JWTSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                           get_username_max_length)
from allauth.account.adapter import get_adapter
from phonenumber_field.serializerfields import PhoneNumberField
from radon.iot.serializers import NestedDispositivoSerializer
from radon.iot.models import Wisol
from .utils import create_user_and_dispositivo

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    dispositivo_set = NestedDispositivoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'dispositivo_set', 'tipo', 'gasera',
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
        return data


class AsistedUserDispositivoCreation(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    gasera = serializers.HiddenField(default='DUMMY')
    tipo = serializers.HiddenField(default='CONSUMIDOR')
    pwdtemporal = serializers.HiddenField(default=True)
    telefono = PhoneNumberField(required=False)
    wisol = serializers.CharField(required=True)
    location = GeometryField(precision=14)
    capacidad = serializers.IntegerField(required=False)

    def validate_gasera(self, gasera):
        return self.context['request'].user.gasera

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
        if self.wisol.activo:
            raise serializers.ValidationError("El chip Wisol ya tiene un dispositivo asignado")
        return serie

    def get_cleaned_data(self):
        user_data = {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'gasera': self.validated_data.get('gasera', None),
            'tipo': self.validated_data.get('tipo'),
            'pwdtemporal': self.validated_data.get('pwdtemporal'),
        }
        disp_data = {
            'wisol': self.wisol,
            'location': self.validated_data.get('location', ''),
            'capacidad': self.validated_data.get('capacidad', None)
        }
        return user_data, disp_data

    def save(self, request):
        user_data, disp_data = self.get_cleaned_data()
        user, dispositivo = create_user_and_dispositivo(user_data, disp_data)
        return user


class ActivateUsers(serializers.Serializer):
    email = serializers.EmailField()
    serie = serializers.CharField()

    def validate_serie(self, serie):
        try:
            self.wisol = Wisol.objects.get(serie=serie)
        except Wisol.DoesNotExist:
            raise serializers.ValidationError(
                'El chip que corresponde al dispositivo no existe '
                'favor de llamar a soporte.'
            )
        return serie

    def validate(self, attrs):
        if hasattr(self, 'wisol'):
            wisol = self.wisol
        else:
            wisol = Wisol.objects.get(attrs['serie'])
        if wisol.dispositivo.usuario.email == attrs['email']:
            raise serializers.ValidationError(
                'Este dispositivo está registrado con otro correo electrónico.'
            )

    def validate_email(self, email):
        try:
            usr = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Tu correo electronico o tu usuario no fueron registrados '
                'correctamente, favor de llamar a soporte'
            )
        if not usr.pwdtemporal or not usr.is_active:
            raise serializers.ValidationError('El correo electrónico del usuario no se encuentra activo.')
        return email
