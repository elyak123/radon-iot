from django.db import models
from radon.georadon.models import Municipio


class Gasera(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    municipio = models.ManyToManyField(Municipio, through='MunicipioGasera')

    @property
    def precio_actual(self):
        return self.municipio.precio.all().order_by('-fecha').first()

    class Meta:
        verbose_name = "Gasera"
        verbose_name_plural = "Gaseras"

    def __str__(self):
        return self.nombre


class MunicipioGasera(models.Model):
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)


class Precio(models.Model):
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now=True)
    municipio_gasera = models.ForeignKey(MunicipioGasera, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"

    def __str__(self):
        return f'${self.precio} {self.gasera.nombre[:16]}'
