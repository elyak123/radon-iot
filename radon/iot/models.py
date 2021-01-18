from django.db.models import OuterRef, Exists, Subquery
from django.core.serializers import serialize
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from radon.users.utils import get_default_user
from radon.market.models import Sucursal
from radon.georadon.models import Municipio, Localidad

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
        qs = Lectura.objects.filter(dispositivo=OuterRef('pk')).order_by('-fecha')[:1]
        return self.annotate(ultima_lectura=Subquery(qs.values('porcentaje'), output_field=models.DecimalField()))

    def calendarizables(self):
        return self.anotar_lecturas().filter(ultima_lectura__lte=20, calendarizado=False)

    def anotar_pedidos_calendarizados(self, jornada):
        from radon.rutas.models import Pedido
        pedidos = Pedido.objects.filter(dispositivo=OuterRef('pk'), jornada=jornada)
        return self.annotate(pedidos_calendarizados=Exists(pedidos))

    def calendarizados(self, jornada):
        return self.anotar_pedidos_calendarizados(jornada).filter(
            sucursal__gasera=jornada.gasera,  # por lo pronto, despues debera ser jornada.sucursal
            pedidos_calendarizados=True
        )

    def calendarizados_geojson(self, jornada):
        return serialize('geojson', self.calendarizados(jornada), geometry_field='location')


class Dispositivo(models.Model):
    STATUS_CHOICES = (
        ("VERDE", "Verde"),
        ("ROJO", "Rojo"),
        ("AMARILLO", "Amarillo")
    )
    # Localidad.objects.filter(geo__intersects=mariel.location.wkt)
    nombre = models.CharField('Nombre del dispositivo', max_length=45, default='Casa')
    wisol = models.OneToOneField(Wisol, on_delete=models.CASCADE)
    capacidad = models.IntegerField('Capacidad del tanque', null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, null=True, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, default=get_default_user, on_delete=models.SET(get_default_user))
    location = models.PointField(null=True)
    calendarizado = models.BooleanField('Indica si se esta a la espera de ser surtido.', default=False)
    tipo = models.IntegerField(default=1)
    status = models.CharField('Status del dispositivo', max_length=25, default='VERDE', choices=STATUS_CHOICES)
    calle = models.CharField(max_length=150, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    cp = models.CharField(max_length=10, null=True, blank=True)
    colonia = models.CharField(max_length=75, null=True, blank=True)

    objects = models.Manager()
    especial = DispositivoSet.as_manager()

    def get_ultima_lectura(self):
        lectura = self.lectura_set.order_by('-fecha').first()
        if lectura:
            return {'lectura': lectura.porcentaje, 'fecha': lectura.fecha}
        return None

    @property
    def wisol__serie(self):
        return self.wisol.serie

    def lecturas_ordenadas(self):
        return self.lectura_set.order_by('-fecha')

    def pedidos_ordenados(self):
        return self.pedido_set.all().select_related('precio').select_related('jornada').order_by('-jornada__fecha')

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def __str__(self):
        return 'Serie: {}'.format(self.wisol.serie)


class Instalacion(models.Model):

    fecha = models.DateTimeField(auto_now=True)
    operario = models.ForeignKey(User, related_name='operario', on_delete=models.CASCADE)
    consumidor = models.ForeignKey(User, related_name='consumidor', on_delete=models.CASCADE)
    folio = models.CharField('Folio de Instalación', max_length=10, unique=True)

    class Meta:
        verbose_name = "Instalacion"
        verbose_name_plural = "Instalaciones"

    def __str__(self):
        return '{} {}'.format(self.fecha, self.operario)


class Lectura(models.Model):
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)
    fecha = models.DateTimeField()
    sensor = models.IntegerField()  # 0 - 4095
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)  # 0 - 100.00%
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"

    def __str__(self):
        return f'{self.fecha.isoformat(timespec="minutes")}-{self.dispositivo.wisol.serie}-{self.porcentaje}%'
