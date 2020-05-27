from django import forms
from radon.rutas.models import Pedido


class PedidoCreationForm(forms.ModelForm):

    class Meta:
        model = Pedido    
        fields = ["cantidad", "dispositivo", "precio", "jornada"]
        widgets = {
            "cantidad": forms.HiddenInput(),
            "dispositivo": forms.HiddenInput(),
            "precio": forms.HiddenInput(),
            "jornada": forms.HiddenInput()
        }