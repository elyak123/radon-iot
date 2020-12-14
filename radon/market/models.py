from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField
from radon.georadon.models import Municipio, Localidad


class Gasera(models.Model):
    nombre = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Gasera"
        verbose_name_plural = "Gaseras"

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(blank=True, max_length=80)
    numeroPermiso = models.CharField(max_length=22, unique=True)
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)
    ubicacion = models.PointField(null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    localidad = models.ManyToManyField(Localidad)
    telefono = PhoneNumberField(blank=True)

    @property
    def precio_actual(self):
        return self.precio_set.all().order_by('-fecha').first()

    def __str__(self):
        if not self.nombre:
            return f'{self.gasera.nombre[:10]} {self.municipio.nombre[:16]}'
        return f'{self.nombre} {self.gasera.nombre[:10]}'


class Precio(models.Model):
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"

    def __str__(self):
        return f'${self.precio} {self.sucursal.gasera.nombre[:16]}'
