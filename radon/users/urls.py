from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path(r'', include(router.urls)),
]
