from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path('user-dispositivo-registration/', views.RegisterUsersView.as_view()),
    path('activacion-usuarios/', views.activacion_usuarios, name='activacion-usuarios'),
    path(r'', include(router.urls)),
]
