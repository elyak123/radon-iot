import floppyforms as forms
from radon.iot.widgets import PointWidget

class GeoForm(forms.Form):
    point = forms.gis.PointField(widget=PointWidget)