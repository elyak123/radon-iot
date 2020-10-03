from django import template

register = template.Library()

@register.filter(name='badge')
def badge(value):
    if not value:
        return "light"
    value = int(value)
    danger = "danger" if value >=0 and value <= 20 else None
    warning = "warning" if value > 20 and value <= 60 else None
    success = "success" if value > 60 and value <= 100 else None
    #return any([danger, warning, success])
    return [x for x in [danger, warning, success] if x is not None][0]
