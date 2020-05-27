import datetime
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.db import connection
from dynamic_validator import ModelFieldRequiredMixin
from radon.users.models import Gasera, Precio
from radon.iot.models import Dispositivo

User = get_user_model()


class Jornada(models.Model):
    fecha = models.DateField(default=datetime.datetime.now)
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)

    def geometria_actualizada(self):
        return self.pedido_set.filter(actualizado=False).exists()

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
        return self.jornada.pedido_set.all().count()

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"

    def __str__(self):
        return 'Ruta: {}'.format(self.jornada.fecha)


class PedidoSet(models.QuerySet):

    def pedidos_por_fecha_creacion_global(self, semana):
        # "2020-W26 (se espera aaaa-Wss)
        start_date = str(datetime.datetime.strptime(semana + '-1', "%Y-W%W-%w"))
        finish_date = str(datetime.datetime.strptime(semana + '-0', "%Y-W%W-%w"))
        sql = '''
        SELECT DATE(fecha_creacion) AS fecha, SUM(cantidad) AS cantidad, "users_gasera"."id" AS gasera
        FROM rutas_pedido
        INNER JOIN "iot_dispositivo" ON "rutas_pedido"."dispositivo_id" = "iot_dispositivo"."id"
        INNER JOIN "users_user" ON "iot_dispositivo"."usuario_id" = "users_user"."id"
        INNER JOIN "users_gasera" ON "users_user"."gasera_id" = "users_gasera"."id"
        WHERE DATE(fecha_creacion) BETWEEN %(start_date)s AND %(finish_date)s
        GROUP BY fecha, "users_gasera"."id"
        ORDER BY fecha DESC, gasera DESC;
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql, {
                'start_date': start_date,
                'finish_date': finish_date})
            qs = cursor.fetchall()
        return qs

    def pedidos_por_dia_global(self, semana):
        # "2020-W26 (se espera aaaa-Wss)
        start_date = str(datetime.datetime.strptime(semana + '-1', "%Y-W%W-%w"))
        finish_date = str(datetime.datetime.strptime(semana + '-0', "%Y-W%W-%w"))
        sql = '''
        SELECT "rutas_jornada"."fecha" as fecha, SUM(cantidad) AS cantidad, "users_gasera"."nombre" AS gasera
        FROM rutas_pedido
        INNER JOIN "rutas_ruta" ON "rutas_pedido"."ruta_id" = "rutas_ruta"."id"
        INNER JOIN "rutas_jornada" ON "rutas_ruta"."jornada_id" = "rutas_jornada"."id"
        INNER JOIN "users_gasera" ON "rutas_jornada"."gasera_id" = "users_gasera"."id"
        WHERE "rutas_jornada"."fecha" BETWEEN %(start_date)s AND %(finish_date)s
        GROUP BY fecha, gasera
        ORDER BY fecha DESC, gasera DESC;
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql, {
                'start_date': start_date,
                'finish_date': finish_date})
            qs = cursor.fetchall()
        return qs

    def pedidos_por_dia_por_gasera(self, gasera, semana):
        # "2020-W26 (se espera aaaa-Wss)
        start_date = str(datetime.datetime.strptime(semana + '-1', "%Y-W%W-%w"))
        finish_date = str(datetime.datetime.strptime(semana + '-0', "%Y-W%W-%w"))
        gasera_id = gasera.id
        sql = '''
        SELECT "rutas_jornada"."fecha" as fecha, SUM(cantidad) AS cantidad
        FROM rutas_pedido
        INNER JOIN "rutas_ruta" ON "rutas_pedido"."ruta_id" = "rutas_ruta"."id"
        INNER JOIN "rutas_jornada" ON "rutas_ruta"."jornada_id" = "rutas_jornada"."id"
        WHERE "rutas_jornada"."fecha" BETWEEN %(start_date)s AND %(finish_date)s
        AND "rutas_jornada"."gasera_id" = %(gasera_id)s
        GROUP BY fecha
        ORDER BY fecha;
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql, {
                'start_date': start_date,
                'finish_date': finish_date,
                'gasera_id': gasera_id})
            qs = cursor.fetchall()
        return qs

    def pedidos_por_fecha_creacion_por_gasera(self, gasera, semana):
        # "2020-W26 (se espera aaaa-Wss)
        start_date = str(datetime.datetime.strptime(semana + '-1', "%Y-W%W-%w"))
        finish_date = str(datetime.datetime.strptime(semana + '-0', "%Y-W%W-%w"))
        gasera_id = gasera.id
        sql = '''
        SELECT DATE(fecha_creacion) AS fecha, SUM(cantidad) AS cantidad
        FROM rutas_pedido
        INNER JOIN "iot_dispositivo" ON "rutas_pedido"."dispositivo_id" = "iot_dispositivo"."id"
        INNER JOIN "users_user" ON "iot_dispositivo"."usuario_id" = "users_user"."id"
        INNER JOIN "users_gasera" ON "users_user"."gasera_id" = "users_gasera"."id"
        WHERE DATE(fecha_creacion) BETWEEN %(start_date)s AND %(finish_date)s
        AND "users_gasera"."id" = %(gasera_id)s
        GROUP BY fecha
        ORDER BY fecha DESC;
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql, {
                'start_date': start_date,
                'finish_date': finish_date,
                'gasera_id': gasera_id})
            qs = cursor.fetchall()
        return qs


class Pedido(ModelFieldRequiredMixin, models.Model):
    fecha_creacion = models.DateTimeField(auto_now=True)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, null=True)
    orden = models.IntegerField('Orden del dispositivo dentro de una ruta.', null=True)
    precio = models.ForeignKey(Precio, on_delete=models.CASCADE)
    actualizado = models.BooleanField(default=False)

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
