import pytz
import datetime
from django.conf import settings
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


class SucursalSet(models.QuerySet):
    def from_localidad(self, loc):
        tz = pytz.timezone(settings.TIME_ZONE)
        now = tz.fromutc(datetime.datetime.utcnow())
        fecha = now - datetime.timedelta(days=30)
        return Precio.objects.filter(localidad=loc, fecha__gr=fecha).values(
            'sucursal__gasera__nombre',
            'sucursal__numeroPermiso',
            'sucursal__telefono'
        )


class Sucursal(models.Model):
    nombre = models.CharField(blank=True, max_length=80)
    numeroPermiso = models.CharField(max_length=22, unique=True)
    gasera = models.ForeignKey(Gasera, on_delete=models.CASCADE)
    ubicacion = models.PointField(null=True)
    telefono = PhoneNumberField(blank=True)

    @property
    def precio_actual(self):
        return self.precio_set.all().order_by('-fecha').first()

    def __str__(self):
        if not self.nombre:
            return f'{self.gasera.nombre[:10]} {self.numeroPermiso}'
        return f'{self.nombre} {self.gasera.nombre[:10]}'

    @property
    def municipios(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        utc_time = datetime.datetime.utcnow()
        days_ago = tz.fromutc(utc_time) - datetime.timedelta(days=60)
        precios = self.precio_set.filter(
            fecha__gt=days_ago, localidad__geo__intersects=models.OuterRef('geo')
        ).values('pk')
        return Municipio.objects.annotate(oferta=models.Exists(precios)).filter(oferta=True)

    @property
    def localidades(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        utc_time = datetime.datetime.utcnow()
        days_ago = tz.fromutc(utc_time) - datetime.timedelta(days=60)
        precios = self.precio_set.filter(
            fecha__gt=days_ago, localidad=models.OuterRef('pk')).values('precio')
        return Localidad.objects.annotate(importes=models.Exists(precios)).filter(importes=True)


class Precio(models.Model):
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"

    def __str__(self):
        return f'${self.precio} {self.localidad.nombre[:16]}'
