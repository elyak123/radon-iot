from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from radon.users.utils import get_default_gasera


class Gasera(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class User(AbstractUser):
    TIPO_USUARIO = (('CLIENTE', 'Cliente'), ('CONSUMIDOR', 'Consumidor'), ('STAFF', 'Staff'))

    telefono = PhoneNumberField(blank=True)
    tipo = models.CharField(max_length=14, choices=TIPO_USUARIO, default='CLIENTE')
    gasera = models.ForeignKey(Gasera, on_delete=models.SET(get_default_gasera))

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
