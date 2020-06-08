from django.contrib.sites.models import Site
from django.db import models


class Sitio(Site):
    modulo = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.domain + " : " + self.modulo
