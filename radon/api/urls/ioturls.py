from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from radon.api import views


####################
#  ROUTER PARA IOT #
####################
iotrouter = routers.DefaultRouter()
iotrouter.register(r'dispositivos', views.APIDeviceViewSet)
iotrouter.register(r'devicetype', views.APIDeviceTypeViewSet)
iotrouter.register(r'wisol', views.APIWisolViewSet)
iotrouter.register(r'instalaciones', views.APIInstalacionViewSet, basename='instalacion')

urlpatterns = [
    ####################
    #  URLS PARA IOT #
    ####################
    path('registro-lectura/', views.api_registrolectura, name='registrolectura'),
    path('disponibilidad-wisol/', views.api_wisol_initial_validation, name='dispwisol'),
    path(r'', include(iotrouter.urls)),
]
if settings.DEBUG:
    urlpatterns += [
        path('mock_lectura/', views.api_mock_lectura, name='mock_lectura'),
    ]
