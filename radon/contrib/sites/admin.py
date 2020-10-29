from django.contrib.sites.models import Site
from django.contrib import admin


class SiteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Site, SiteAdmin)
