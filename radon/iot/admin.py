from django.contrib import admin
from django.utils.html import format_html
from .models import Dispositivo, Wisol, DeviceType

# Register your models here.


class Leadsadmin(admin.ModelAdmin):
    list_display = ('serie', 'gasera', 'usuario', 'medida_actual', 'enviar_notificacion')

    def usuario(self, obj):
        return (obj.usuario.name + obj.usuario.lastname)

    def serie(self, obj):
        return obj.wisol.serie

    def gasera(self, obj):
        return obj.usuario.gasera or None

    def medida_actual(self, obj):
        lectura = obj.get_ultima_lectura()
        return None if not lectura else "lectura: " + str(lectura['lectura']) + " fecha: " + lectura['fecha'].strftime("%m/%d/%Y, %H:%M:%S")

    def enviar_notificacion(self, obj):
        return format_html('<a class="addlink" href="#">Enviar</a>')


class WisolAdmin(admin.ModelAdmin):
    list_display = ('serie', 'pac', 'prototype', 'deviceTypeId')


class DeviceTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dispositivo, Leadsadmin)
admin.site.register(Wisol, WisolAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
