from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        pass


class Dispositivo(models.Model):
    # ubicacion = Pendiente
    n_serie = models.CharField(max_length=45)
    capacidad = models.IntegerField()
    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def __str__(self):
        pass
    

class Lectura(models.Model):
    fecha = models.DateTimeField()
    nivel = models.IntegerField() # 0 - 100
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"

    def __str__(self):
        return "Disp:{}, {}%".format(self.dispositivo, self.nivel)


