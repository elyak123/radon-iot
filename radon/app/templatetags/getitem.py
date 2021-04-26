
from django import template

register = template.Library()


@register.filter
def getitem(arr, idx):
    return arr[idx]
