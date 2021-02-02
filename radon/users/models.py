from django.contrib.gis.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from radon.market.models import Sucursal


class UserSet(models.QuerySet):

    def leads(self, sucursal):
        from radon.iot.models import Dispositivo
        u_lectura = Dispositivo.especial.filter(
            usuario=models.OuterRef('pk')
        ).calendarizables().filter(sucursal=sucursal).values('ultima_lectura')[:1]
        disps = Dispositivo.especial.filter(
            usuario=models.OuterRef('pk')
        ).calendarizables().filter(sucursal=sucursal).values('wisol__serie')[:1]
        return self.filter(tipo='CONSUMIDOR').annotate(
            ultima_lectura=models.Subquery(u_lectura, output_field=models.IntegerField())
        ).annotate(
            serie=models.Subquery(disps, output_field=models.IntegerField())
        ).filter(ultima_lectura__isnull=False, serie__isnull=False)


class User(AbstractUser):
    Types = (('CLIENTE', 'Cliente'), ('CONSUMIDOR', 'Consumidor'), ('STAFF', 'Staff'), ('OPERARIO', 'Operario'))

    telefono = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    tipo = models.CharField(max_length=14, choices=Types, default='CONSUMIDOR')
    pwdtemporal = models.BooleanField(default=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()
    especial = UserSet.as_manager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            self.tipo = self.base_type
        return super().save(*args, **kwargs)


class RadonBaseUserManager(UserManager):
    is_staff = False
    is_superuser = False

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields['is_staff'] = self.is_staff
        extra_fields['is_superuser'] = self.is_superuser
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        if not self.is_superuser:
            raise ValueError('Este tipo de usuario no puede ser Super User')
        return super().RadonBaseUserManager.create_superuser(username, email, password, **extra_fields)


class ConsumidorManager(RadonBaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(tipo='CONSUMIDOR')


class Consumidor(User):
    base_type = 'CONSUMIDOR'
    objects = ConsumidorManager()

    @property
    def hola(self):
        print('hola desde consumidor')

    class Meta:
        proxy = True
        verbose_name = "Consumidor"
        verbose_name_plural = "Consumidores"


class ClienteManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(tipo='CLIENTE')


class Cliente(User):
    base_type = 'CLIENTE'
    objects = ClienteManager()

    class Meta:
        proxy = True
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class OperadorManager(RadonBaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(tipo='OPERARIO')


class Operador(User):
    base_type = 'OPERARIO'
    objects = OperadorManager()

    class Meta:
        proxy = True
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"


class StaffManager(RadonBaseUserManager):
    is_staff = True
    is_superuser = False

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(tipo='STAFF')


class Staff(User):
    base_type = 'STAFF'
    objects = StaffManager()

    class Meta:
        proxy = True
        verbose_name = "Staff"
        verbose_name_plural = "Staff"


class SuperUserManager(RadonBaseUserManager):
    is_staff = True
    is_superuser = True

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(tipo='STAFF', is_superuser=True)


class SuperUser(User):
    base_type = 'STAFF'
    objects = SuperUserManager()

    class Meta:
        proxy = True
        verbose_name = "Super Usuario"
        verbose_name_plural = "Super Usuarios"
