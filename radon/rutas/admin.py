from django.contrib import admin
from django.utils.html import format_html
from .models import Pedido

# Register your models here.


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'dispositivo', 'cantidad', 'jornada', 'gasera')
    search_fields = ("dispositivo__usuario__gasera__nombre__icontains", 'dispositivo__usuario__username__icontains', 'dispositivo__wisol__serie__icontains')

    def gasera(self, obj):
        return obj.dispositivo.usuario.gasera

    def usuario(self, obj):
        return obj.dispositivo.usuario

    def telefono(self, obj):
        return format_html('<a href="tel:{}">{}</a>', obj.dispositivo.usuario.telefono, obj.dispositivo.usuario.telefono)


admin.site.register(Pedido, PedidoAdmin)
