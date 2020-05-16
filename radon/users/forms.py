from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from radon.users.models import User


class UserForm(UserCreationForm):
    tipo = forms.ChoiceField(
        choices=[('CLIENTE', 'Cliente'), ('OPERARIO','Operario')],
        required=True
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', "password1", "password2", 'telefono', 'tipo']


class UserUpdateForm(UserChangeForm):
    tipo = forms.ChoiceField(
        choices=[('CLIENTE', 'Cliente'), ('OPERARIO','Operario')],
        required=True
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'tipo']

