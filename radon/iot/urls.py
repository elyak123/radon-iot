from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'iot'

router = routers.DefaultRouter()
router.register(r'dispositivos', views.DeviceViewSet)
router.register(r'devicetype', views.DeviceTypeViewSet)

urlpatterns = [
    path('lectura/', views.lectura, name='lectura'),
    path(r'', include(router.urls)),
]
