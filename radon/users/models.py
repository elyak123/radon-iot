from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from radon.users.utils import get_default_gasera


class Gasera(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class User(AbstractUser):
    TIPO_USUARIO = (('CLIENTE', 'Cliente'), ('CONSUMIDOR', 'Consumidor'), ('STAFF', 'Staff'))

    telefono = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    tipo = models.CharField(max_length=14, choices=TIPO_USUARIO, default='CLIENTE')
    gasera = models.ForeignKey(Gasera, default=get_default_gasera, on_delete=models.SET(get_default_gasera))
    pwdtemporal = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
