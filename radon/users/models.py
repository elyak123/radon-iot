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
    TIPO_USUARIO = (('CLIENTE', 'Cliente'), ('CONSUMIDOR', 'Consumidor'), ('STAFF', 'Staff'), ('OPERARIO', 'Operario'))

    telefono = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    tipo = models.CharField(max_length=14, choices=TIPO_USUARIO, default='CLIENTE')
    pwdtemporal = models.BooleanField(default=False)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()
    especial = UserSet.as_manager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
