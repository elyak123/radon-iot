from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from radon.users.models import Gasera
from radon.iot.models import Dispositivo

User = get_user_model()


class Jornada(models.Model):
    fecha = models.DateField(auto_now=True)
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"

    def __str__(self):
        pass


class Vehiculo(models.Model):
    placa = models.CharField(max_length=12)
    n_economico = models.CharField(max_length=12, blank=True)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"

    def __str__(self):
        pass


class Ruta(models.Model):
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    geometry = models.LineStringField()
    dispositivo = models.ManyToManyField(Dispositivo, through='DispositivoRuta')
    vehiculo = models.ManyToManyField(Vehiculo)

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"

    def __str__(self):
        pass


class DispositivoRuta(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    orden = models.IntegerField('Orden del dispositivo dentro de una ruta.')

    class Meta:
        verbose_name = "DispositivoRuta"
        verbose_name_plural = "DispositivoRutas"

    def __str__(self):
        pass
