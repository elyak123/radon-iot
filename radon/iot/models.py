from django.db.models import OuterRef, Exists, Subquery, F
from django.core.serializers import serialize
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from radon.users.utils import get_default_user

User = get_user_model()


class DeviceType(models.Model):
    key = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)

    class Meta:
        verbose_name = "DeviceType"
        verbose_name_plural = "DeviceTypes"

    def __str__(self):
        return self.name


class Wisol(models.Model):
    serie = models.CharField(max_length=8, unique=True)
    pac = models.CharField(max_length=16)
    prototype = models.BooleanField(default=True)
    deviceTypeId = models.ForeignKey(DeviceType, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Wisol"
        verbose_name_plural = "Wisols"

    def __str__(self):
        return self.serie

    @property
    def activo(self):
        return hasattr(self, 'dispositivo')


class DispositivoSet(models.QuerySet):

    def anotar_lecturas(self):
        qs = Lectura.objects.filter(dispositivo=OuterRef('pk')).order_by('-fecha').first()
        return self.annotate(ultima_lectura=Subquery(qs.values('nivel'), output_field=models.IntegerField()))

    def calendarizables(self, gasera):
        return self.filter(ultima_lectura__lte=F(20), calendarizado=False, gasera=gasera).anotar_lecturas()

    def anotar_pedidos_calendarizados(self, jornada):
        from radon.rutas.models import Pedido
        pedidos = Pedido.objects.filter(dispositivo=OuterRef('pk'), jornada=jornada)
        return self.annotate(pedidos_calendarizados=Exists(pedidos))

    def calendarizados(self, jornada):
        return self.anotar_pedidos_calendarizados(jornada).filter(
            usuario__gasera=jornada.gasera,
            pedidos_calendarizados=True
        )

    def calendarizados_geojson(self, jornada):
        return serialize('geojson', self.calendarizados(jornada), geometry_field='location')


class Dispositivo(models.Model):
    wisol = models.OneToOneField(Wisol, on_delete=models.CASCADE)
    capacidad = models.IntegerField('Capacidad del tanque', null=True)
    usuario = models.ForeignKey(User, default=get_default_user, on_delete=models.SET(get_default_user))
    location = models.PointField(null=True)
    calendarizado = models.BooleanField('Indica si se esta a la espera de ser surtido.', default=False)

    objects = models.Manager()
    especial = DispositivoSet.as_manager()

    def get_ultima_lectura(self):
        return self.lectura_set.order_by('-fecha').first()

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def __str__(self):
        return 'Dispositivo {}'.format(self.wisol.serie)


class Instalacion(models.Model):

    fecha = models.DateTimeField(auto_now=True)
    operario = models.ForeignKey(User, related_name='operario', on_delete=models.CASCADE)
    consumidor = models.ForeignKey(User, related_name='consumidor', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Instalacion"
        verbose_name_plural = "Instalaciones"

    def __str__(self):
        return '{} {}'.format(self.fecha, self.operario)


class Lectura(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    nivel = models.IntegerField()  # 0 - 100
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"

    def __str__(self):
        return "Disp:{}, {}%".format(self.dispositivo, self.nivel)
