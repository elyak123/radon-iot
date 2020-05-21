from django.conf import settings
import floppyforms as forms


class PointWidget(forms.gis.PointWidget, forms.gis.BaseGMapWidget):
    template_name = 'iot/PointWidgetTemplate.html'
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
