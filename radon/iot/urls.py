from django.urls import path
from rest_framework import routers
from . import views

app_name = 'iot'

router = routers.DefaultRouter()
router.register(r'dispositivos', views.DeviceViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('lectura/', views.lectura, name='lectura'),
]
