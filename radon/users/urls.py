from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('detalle/<username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('editar/<username>/', views.UserUpdateView.as_view(), name='user_update'),
    path('eliminar/<username>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('nuevo/', views.UserCreateView.as_view(), name='user_creation'),

    ##################
    #  URLS PARA API #
    ##################
    path('user-dispositivo-registration/', views.RegisterUsersView.as_view(), name='usr-disp-reg'),
    path('activacion-usuarios/', views.activacion_usuarios, name='activacion-usuarios'),
    path('leads/', views.LeadsView.as_view(), name='leads'),
    path(r'', include(router.urls)),
]
