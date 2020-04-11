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


class Dispositivo(models.Model):
    serie = models.CharField(max_length=45, unique=True)
    capacidad = models.IntegerField('Capacidad del tanque', null=True)
    usuario = models.ForeignKey(User, default=get_default_user, on_delete=models.SET(get_default_user))
    location = models.PointField(null=True)
    deviceTypeId = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    pac = models.CharField(max_length=80)
    prototype = models.BooleanField(default=True)

    def get_ultima_lectura(self):
        return self.lectura_set.order_by('-fecha').first()

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def __str__(self):
        return 'Dispositivo {}'.format(self.serie)


class Lectura(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    nivel = models.IntegerField()  # 0 - 100
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"

    def __str__(self):
        return "Disp:{}, {}%".format(self.dispositivo, self.nivel)
