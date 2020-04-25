from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'iot'

router = routers.DefaultRouter()
router.register(r'dispositivos', views.DeviceViewSet)
router.register(r'devicetype', views.DeviceTypeViewSet)
router.register(r'wisol', views.WisolViewSet)
router.register(r'instalaciones', views.InstalacionViewSet, basename='instalacion')

urlpatterns = [
    path('registro-lectura/', views.registrolectura, name='registrolectura'),
    path(r'', include(router.urls)),
]
