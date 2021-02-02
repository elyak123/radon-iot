from django import forms
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from radon.users.models import User


class UserForm(UserCreationForm):
    tipo = forms.ChoiceField(
        choices=[('CLIENTE', 'Cliente'), ('OPERARIO', 'Operario')],
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', "password1", "password2", 'telefono', 'tipo']


class UserUpdateForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            'Las contraseñas no se almacenan en texto plano, así '
            'que no hay manera de ver la contraseña del usuario, pero se puede '
            'cambiar la contraseña mediante este '
            '<a href="{}">formulario</a>.'
        ),
    )

    def __init__(self, user, *args, **kwargs):
        # Llamamos el super del padre porque el padre cambia arbitrariamente la url
        # de cambio de contraseña
        super(UserChangeForm, self).__init__(*args, **kwargs)
        pass_change = reverse('account_change_password')
        self.fields['password'].help_text = self.fields['password'].help_text.format(pass_change)
        self.user = user

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono']
