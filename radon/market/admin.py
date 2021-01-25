from django.contrib import admin
from radon.market.models import Precio, Gasera


class GaseraAdmin(admin.ModelAdmin):
    pass


class PrecioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'sucursal', 'precio', 'localidad')

    def get_queryset(self, request):
        queryset = super(PrecioAdmin, self).get_queryset(request)
        # you logic here to `annotate`the queryset with income
        return queryset


admin.site.register(Precio, PrecioAdmin)
admin.site.register(Gasera, GaseraAdmin)
