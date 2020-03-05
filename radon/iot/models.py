from django.db import models


class DeviceType(models.Model):
    key = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)

    class Meta:
        verbose_name = "DeviceType"
        verbose_name_plural = "DeviceTypes"

    def __str__(self):
        pass


class Dispositivo(models.Model):
    # ubicacion = Pendiente
    serie = models.CharField(max_length=45, unique=True)
    capacidad = models.IntegerField('Capacidad del tanque', blank=True)
    deviceTypeId = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    pac = models.CharField(max_length=80)
    prototype = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def __str__(self):
        pass


class Lectura(models.Model):
    fecha = models.DateTimeField()
    nivel = models.IntegerField()  # 0 - 100
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"

    def __str__(self):
        return "Disp:{}, {}%".format(self.dispositivo, self.nivel)
