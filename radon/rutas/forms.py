from django import forms
from radon.rutas.models import Pedido


class PedidoCreationForm(forms.ModelForm):

    class Meta:
        model = Pedido    
        fields = '__all__'
