from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserForm
from .models import Precio, Gasera

User = get_user_model()


class UserAdmin(UserAdmin):
    add_form = UserForm
    prepopulated_fields = {'username': ('first_name', 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', 'tipo',),
        }),
    )


class GaseraAdmin(admin.ModelAdmin):
    pass


class PrecioAdmin(admin.ModelAdmin):
    pass

# Re-register UserAdmin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)
admin.site.register(Precio, PrecioAdmin)
admin.site.register(Gasera, PrecioAdmin)
