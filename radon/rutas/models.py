from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from dynamic_validator import ModelFieldRequiredMixin
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
        return 'Jornada: {}'.format(self.fecha)


class Vehiculo(models.Model):
    placa = models.CharField(max_length=12)
    n_economico = models.CharField(max_length=12, blank=True)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"

    def __str__(self):
        return self.placa


class Ruta(models.Model):
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    geometry = models.LineStringField()
    vehiculo = models.ManyToManyField(Vehiculo)

    def cantidad_pedidos(self):
        return self.pedido_set.all().count()

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"

    def __str__(self):
        return 'Ruta: {}'.format(self.jornada.fecha)


class Pedido(ModelFieldRequiredMixin, models.Model):
    fecha_creacion = models.DateTimeField(auto_now=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, null=True)
    orden = models.IntegerField('Orden del dispositivo dentro de una ruta.', null=True)

    CONDITIONAL_REQUIRED_FIELDS = [
        (
            lambda instance: bool(instance.ruta), ['orden'],
        ),
    ]

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return 'Pedido: {}'.format(self.cantidad)
