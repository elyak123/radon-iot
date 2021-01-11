
from django import template

register = template.Library()


@register.filter
def mul(num, val):
    return num * val
