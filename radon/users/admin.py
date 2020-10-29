from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = fields = ['username', 'first_name', 'last_name', 'email', "password1", "password2", 'telefono', 'tipo']


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name', 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', ),
        }),
    )


# Re-register UserAdmin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)
