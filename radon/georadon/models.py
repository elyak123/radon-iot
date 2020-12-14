from django.contrib.gis.db import models


class Estado(models.Model):
    nombre = models.CharField(max_length=45, unique=True)


class Municipio(models.Model):
    clave = models.CharField(max_length=5, unique=True)
    nombre = models.CharField(max_length=90, unique=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    geo = models.MultiPolygonField(geography=True)


class Localidad(models.Model):
    geo = models.MultiPolygonField(geography=True)
    nombre = models.CharField(max_length=80)
    clave = models.CharField(max_length=13, unique=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    @property
    def descompuesto(self):
        return (self.clave[0:2], self.clave[0:5], self.clave)
