from django.contrib.gis.db import models


class Estado(models.Model):
    nombre = models.CharField(max_length=45, unique=True)


class Municipio(models.Model):
    clave = models.CharField(max_length=15)
    nombre = models.CharField(max_length=90, unique=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    geo = models.MultiPolygonField(geography=True)

    class Meta:
        unique_together = ('clave', 'estado')


class Localidad(models.Model):
    geo = models.PolygonField(geography=True)
    nombre = models.CharField(max_length=80)
    clave = models.CharField(max_length=15)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('clave', 'municipio')
