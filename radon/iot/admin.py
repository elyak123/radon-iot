from django.contrib.gis import admin
from django.utils.html import format_html
from .models import Dispositivo, Wisol, DeviceType, Lectura, Firmware, Hardware
from radon.iot.widgets import PointWidget


class LecturaInLine(admin.TabularInline):
    model = Lectura
    extra = 0

    def get_queryset(self, request):
        qs = super(LecturaInLine, self).get_queryset(request)
        ids = qs.values('pk')[:60]
        qs = Lectura.objects.filter(pk__in=ids).order_by('-id')
        return qs


class DispositivoAdmin(admin.OSMGeoAdmin):
    inlines = [
        LecturaInLine
    ]
    exclude = ['location']
    map_srid = 4326

    list_display = ('serie', 'usuario', 'medida_actual', 'enviar_notificacion')

    def get_map_widget(self, db_field):
        return PointWidget

    def usuario(self, obj):
        return (obj.usuario.name + obj.usuario.lastname)

    def serie(self, obj):
        return obj.wisol.serie

    def medida_actual(self, obj):
        lectura = obj.get_ultima_lectura()
        return None if not lectura else "lectura: " + str(lectura['lectura']) + " fecha: " + lectura['fecha'].strftime("%m/%d/%Y, %H:%M:%S")

    def enviar_notificacion(self, obj):
        return format_html('<a class="addlink" href="#">Enviar</a>')


class WisolAdmin(admin.ModelAdmin):
    list_display = ('serie', 'pac', 'prototype', 'deviceTypeId')


class DeviceTypeAdmin(admin.ModelAdmin):
    pass


class FirmwareAdmin(admin.ModelAdmin):
    pass


class HardwareAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dispositivo, DispositivoAdmin)
admin.site.register(Wisol, WisolAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Firmware, FirmwareAdmin)
admin.site.register(Hardware, HardwareAdmin)
