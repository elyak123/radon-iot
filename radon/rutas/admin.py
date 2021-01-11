from django.contrib import admin
from django.utils.html import format_html
from .models import Pedido, Mensaje
from django.utils.functional import curry


# Register your models here.
class MensajeInLine(admin.TabularInline):
    model = Mensaje

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if request.method == "GET":
            initial.append({
                'autor': request.user
            })
        formset = super(MensajeInLine, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset


class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        MensajeInLine
    ]
    list_display = ('usuario', 'telefono', 'dispositivo', 'cantidad', 'jornada', 'precio', 'gasera')
    search_fields = ("dispositivo__usuario__gasera__nombre__icontains",
                     'dispositivo__usuario__username__icontains',
                     'dispositivo__wisol__serie__icontains')

    def usuario(self, obj):
        return obj.dispositivo.usuario

    def gasera(self, obj):
        return obj.precio.sucursal.gasera

    def telefono(self, obj):
        return format_html('<a href="tel:{}">{}</a>',
                           obj.dispositivo.usuario.telefono,
                           obj.dispositivo.usuario.telefono
                           )


admin.site.register(Pedido, PedidoAdmin)
