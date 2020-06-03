from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from radon.users.utils import get_default_gasera


class Gasera(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    capacidad_total = models.IntegerField('Capacidad total de distribucion', null=True)

    @property
    def precio_actual(self):
        return self.precio_set.filter(actual=True).first()

    class Meta:
        verbose_name = "Gasera"
        verbose_name_plural = "Gaseras"

    def __str__(self):
        return self.nombre


class Precio(models.Model):
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)
    actual = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"
        unique_together = ('gasera', 'actual')

    def __str__(self):
        return f'${self.precio} {self.gasera.nombre[:16]}... Actual: {self.actual}'


class UserSet(models.QuerySet):

    def leads(self, gasera):
        from radon.iot.models import Dispositivo
        u_lectura = Dispositivo.especial.filter(
            usuario=models.OuterRef('pk')
        ).calendarizables().values('ultima_lectura')[:1]
        disps = Dispositivo.especial.filter(
            usuario=models.OuterRef('pk')
        ).calendarizables().values('wisol__serie')[:1]
        return self.filter(gasera=gasera, tipo='CONSUMIDOR').annotate(
            ultima_lectura=models.Subquery(u_lectura, output_field=models.IntegerField())
        ).annotate(
            serie=models.Subquery(disps, output_field=models.IntegerField())
        ).filter(ultima_lectura__isnull=False)


class User(AbstractUser):
    TIPO_USUARIO = (('CLIENTE', 'Cliente'), ('CONSUMIDOR', 'Consumidor'), ('STAFF', 'Staff'), ('OPERARIO', 'Operario'))

    telefono = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    tipo = models.CharField(max_length=14, choices=TIPO_USUARIO, default='CLIENTE')
    gasera = models.ForeignKey(Gasera, default=get_default_gasera, on_delete=models.SET(get_default_gasera))
    pwdtemporal = models.BooleanField(default=False)

    especial = UserSet.as_manager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
