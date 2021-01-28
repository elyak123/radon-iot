
from django import template
from radon.market import models

register = template.Library()


@register.filter
def lastprecio(permiso):
    return models.Sucursal.objects.get(numeroPermiso=permiso).precio_set.last().precio
