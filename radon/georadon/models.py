from django.contrib.gis.db import models


class Estado(models.Model):
    nombre = models.CharField(max_length=45, unique=True)


class Municipio(models.Model):
    clave = models.CharField(max_length=15)
    nombre = models.CharField(max_length=90)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    geo = models.MultiPolygonField(geography=True)
