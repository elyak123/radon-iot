import datetime
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.db import connection
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


class PedidoSet(models.QuerySet):

    def pedidos_por_dia(self, gasera, semana):
        # "2013-W26 (se espera aaaa-Wss)
        fecha_inicial = datetime.datetime.strptime(semana + '-1', "%Y-W%W-%w")
        fecha_final = datetime.datetime.strptime(semana + '-0', "%Y-W%W-%w")
        sql = '''
        SELECT DATE(fecha_creacion) AS fecha, SUM(cantidad) AS cantidad
        FROM rutas_pedido
        WHERE DATE(fecha_creacion) BETWEEN %(fecha_inicial)s AND %(fecha_final)s GROUP BY fecha;
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql, {'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final})
            qs = cursor.fetchall()
        return qs


class Pedido(ModelFieldRequiredMixin, models.Model):
    fecha_creacion = models.DateTimeField(auto_now=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, null=True)
    orden = models.IntegerField('Orden del dispositivo dentro de una ruta.', null=True)

    objects = models.Manager()
    especial = PedidoSet.as_manager()

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
