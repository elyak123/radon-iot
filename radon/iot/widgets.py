import floppyforms as forms


class PointWidget(forms.gis.PointWidget, forms.gis.BaseGMapWidget):
    google_maps_api_key = 'AIzaSyCF1pVeqP7ihDYESHqcBD-te81dC-m7roI'
