from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path('user-dispositivo-registration/', views.RegisterUsersView.as_view(), name='usr-disp-reg'),
    path('activacion-usuarios/', views.activacion_usuarios, name='activacion-usuarios'),
    path('nuevo/', views.UserCreateView.as_view(), name='user_creation'),
    path('listado/', views.UserListView.as_view(), name='user_list'),
    path(r'', include(router.urls)),
]
