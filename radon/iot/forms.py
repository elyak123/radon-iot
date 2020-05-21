import floppyforms.__future__ as forms
from radon.iot.widgets import PointWidget
from radon.iot import models


class DispositivoForm(forms.ModelForm):
    location = forms.gis.PointField(widget=PointWidget)

    class Meta:
        model = models.Dispositivo
        fields = ['location', 'capacidad']
