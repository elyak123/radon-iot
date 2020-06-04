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
from radon.iot.serializers import NestedDispositivoSerializer, WisolValidation
from radon.iot.models import Wisol
from .utils import create_user_and_dispositivo

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    dispositivo_set = NestedDispositivoSerializer(many=True, read_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'password',
            'email', 'telefono', 'dispositivo_set', 'tipo', 'gasera',
        ]
        depth = 2


class LeadSerializer(serializers.ModelSerializer):
    dispositivo_set = NestedDispositivoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'dispositivo_set', 'tipo', 'gasera',
        ]
        read_only_fields = fields
        depth = 2


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


class AsistedUserDispositivoCreation(WisolValidation):
    """
    ENDPOINT:
    /users/user-dispositivo-registration/

    DESCRIPCION:
    Este endpoint es para crear el usuario con password inutilizable y el dispositivo del chip wisol
    que se esta instalando. El dispositivo deberá de comenzar a funcionar pero el usuario aún necesita
    activación.

    CAMPOS:
    username: Nombre de usuario del futuro usuario
    email: Correo del futuro usuario
    telefono: (string) Telefono del futuro usuario a 10 digitos
    location: (string) Ubicacion geografica del futuro dispositivo en formato POINT(x.abcd -y.xyz)
    capacidad: (int) Capacidad del tanque del futuro dispositivo

    CAMPOS OCULTOS (NO UTILIZABLES PARA EL CLIENTE)
    gasera: (<Gasera: Model>) Sera la gasera del cliente que da de alta el consumidor
    tipo: (string) En este caso siempre será `CONSUMIDOR`
    pwdtemporal: (bool) En este caso siempre será True

    VALIDA:
    * Wisol con serie existe
    * Wisol disponible (sin dispositivo o Usuario)
    * Username sigue convenciones UTF-8
    * Username no existe previo a la creación
    * Email no existe previo a la creación

    ACCIONES:
    * Crea el usuario con pwd no utilizable
    * Crea el dispositivo con el chip Wisol proporcionado
    * Asigna el dispositivo al usuario recién creado
    """
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
    location = GeometryField(precision=14)
    capacidad = serializers.IntegerField(required=False)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_gasera(self, gasera):
        return self.context['request'].user.gasera

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

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


class ActivateUsers(WisolValidation):
    """
    ENDPOINT:
    /users/activacion-usuarios/
    wisol: <serie>
    email: <bla@hola.com>
    password1: pwd
    password2: pwd

    VALIDA:
    * Usuario existe
    * Wisol existe
    * Wisol fue asignado al usuario
    * Los pwd son iguales

    ACCIONES:
    * Establece pwd
    * Quita bandera `pwdtemporal`
    * Pone bandera `is_active`
    * Guarda en DB
    """
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate_email(self, email):
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Tu correo electronico o tu usuario no fueron registrados '
                'correctamente, favor de llamar a soporte'
            )
        if not self.user.pwdtemporal or not self.user.is_active:
            raise serializers.ValidationError(
                'El correo electrónico del usuario no se encuentra pendiente de activación.')
        return email

    def validate_wisol(self, serie):
        self.wisol = self.get_wisol_or_error(serie)
        return serie

    def clean_wisol_email(self, attrs):
        if not hasattr(self, 'wisol'):
            self.wisol = self.get_wisol_or_error(attrs['serie'])
            try:
                if self.wisol.dispositivo.usuario.email != attrs['email']:
                    raise serializers.ValidationError(
                        'Este dispositivo está registrado con otro correo electrónico.'
                    )
            except Wisol.dispositivo.RelatedObjectDoesNotExist:
                raise serializers.ValidationError(
                    'Este chip no ha sido dado de alta correctamente'
                )

    def clean_passwords(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('Los campos de password no coinciden.')
        self.pwd = attrs['password1']

    def validate(self, attrs):
        self.clean_wisol_email(attrs)
        self.clean_passwords(attrs)
        return attrs

    def save(self):
        self.user.set_password(self.pwd)
        self.user.pwdtemporal = False
        self.user.is_active = True
        self.user.save()
        return self.user
