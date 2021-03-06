from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists,
                           get_username_max_length)
from allauth.account.adapter import get_adapter
from phonenumber_field.serializerfields import PhoneNumberField
from radon.iot.serializers import NestedDispositivoSerializer, WisolValidation
from radon.iot.models import Wisol
from .utils import create_user_and_dispositivo, create_user_password, get_localidad_from_wkt

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
            'email', 'telefono', 'dispositivo_set', 'tipo',
        ]
        depth = 2


class LeadSerializer(serializers.ModelSerializer):
    dispositivo_set = NestedDispositivoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telefono', 'dispositivo_set', 'tipo', 'sucursal',
        ]
        read_only_fields = fields
        depth = 2


class EmailValidator(serializers.Serializer):
    """
    ENDPOINT:
    /users/email-validator/

    DESCRIPCION
    Email verificamos que el email no exista en la base de datos
    """
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email


class UsernameValidator(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username


class AsistedUserDispositivoCreation(WisolValidation, EmailValidator, UsernameValidator):
    """
    ENDPOINT:
    /users/user-dispositivo-registration/

    DESCRIPCION:
    Este endpoint es para crear el usuario con password inutilizable y el dispositivo del chip wisol
    que se esta instalando. El dispositivo deber?? de comenzar a funcionar pero el usuario a??n necesita
    activaci??n.

    CAMPOS:
    telefono: (string) Telefono del futuro usuario a 10 digitos
    location: (string) Ubicacion geografica del futuro dispositivo en formato POINT(x.abcd -y.xyz)
    capacidad: (int) Capacidad del tanque del futuro dispositivo
    calle: (string) Nombre de la calle del dispositivo
    numero: (string) Numero e interior si existe
    cp: (string) C??digo postal
    colonia: (string) Colonia de la ubicaci??n del dispositivo

    CAMPOS OCULTOS (NO UTILIZABLES PARA EL CLIENTE)
    sucursal: (<Sucursal: Model>) Sera la sucursal del cliente que da de alta el consumidor
    tipo: (string) En este caso siempre ser?? `CONSUMIDOR`
    pwdtemporal: (bool) En este caso siempre ser?? True

    CAMPOS EN HERENCIA:
    username: Nombre de usuario del futuro usuario
    email: Correo del futuro usuario
    wisol: Numero de serie del wisol a validar y unir al dispositivo

    VALIDA:
    * Wisol con serie existe
    * Wisol disponible (sin dispositivo o Usuario)
    * Username sigue convenciones UTF-8
    * Username no existe previo a la creaci??n
    * Email no existe previo a la creaci??n

    ACCIONES:
    * Crea el usuario con pwd no utilizable
    * Crea el dispositivo con el chip Wisol proporcionado
    * Asigna el dispositivo al usuario reci??n creado
    """

    sucursal = serializers.HiddenField(default='DUMMY')
    tipo = serializers.HiddenField(default='CONSUMIDOR')
    pwdtemporal = serializers.HiddenField(default=True)
    telefono = PhoneNumberField(required=False)
    location = GeometryField(precision=14)
    capacidad = serializers.IntegerField(required=False)
    calle = serializers.CharField()
    numero = serializers.CharField()
    cp = serializers.CharField()
    colonia = serializers.CharField()

    def validate_sucursal(self, sucursal):
        if hasattr(self.context['request'].user, 'sucursal'):
            return self.context['request'].user.sucursal
        else:
            return None

    def get_cleaned_data(self):
        user_data = {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'tipo': self.validated_data.get('tipo'),
            'pwdtemporal': self.validated_data.get('pwdtemporal'),
        }
        disp_data = {
            'wisol': self.wisol,
            'location': self.validated_data.get('location', ''),
            'sucursal': self.validated_data.get('sucursal', None),
            'capacidad': self.validated_data.get('capacidad', None),
            'calle': self.validated_data.get('calle', ''),
            'numero': self.validated_data.get('numero', ''),
            'cp': self.validated_data.get('cp', ''),
            'colonia': self.validated_data.get('colonia', '')
        }
        loc = get_localidad_from_wkt(self.validated_data.get('location'))
        disp_data['localidad'] = loc
        disp_data['municipio'] = loc.municipio
        return user_data, disp_data

    def save(self, request):
        user_data, disp_data = self.get_cleaned_data()
        user, dispositivo = create_user_and_dispositivo(user_data, disp_data)
        return user


class TemporalPassUserDispsitivoCreation(AsistedUserDispositivoCreation):
    password = serializers.HiddenField(default=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['password'] = self.pwd
        return ret

    def get_cleaned_data(self):
        user_data, disp_data = super().get_cleaned_data()
        self.pwd = create_user_password()
        user_data['password'] = self.pwd
        return user_data, disp_data


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
                'El correo electr??nico del usuario no se encuentra pendiente de activaci??n.')
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
                        'Este dispositivo est?? registrado con otro correo electr??nico.'
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
