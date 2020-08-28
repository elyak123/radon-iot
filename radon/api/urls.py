from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from . import views

app_name = 'api'

#####################
#  ROUTER PARA USER #
#####################
usersrouter = routers.DefaultRouter()
usersrouter.register(r'', views.UserViewSet, basename='user')

####################
#  ROUTER PARA IOT #
####################
iotrouter = routers.DefaultRouter()
iotrouter.register(r'dispositivos', views.DeviceViewSet)
iotrouter.register(r'devicetype', views.DeviceTypeViewSet)
iotrouter.register(r'wisol', views.WisolViewSet)
iotrouter.register(r'instalaciones', views.InstalacionViewSet, basename='instalacion')

urlpatterns = [
    ####################
    #  URLS PARA IOT #
    ####################
    path('iot/registro-lectura/', views.registrolectura, name='registrolectura'),
    path('iot/disponibilidad-wisol/', views.wisol_initial_validation, name='dispwisol'),
    path(r'iot/', include(iotrouter.urls)),

    ####################
    #  URLS PARA USERS #
    ####################
    path('users/user-dispositivo-registration/', views.RegisterUsersView.as_view(), name='usr-disp-reg'),
    path('users/activacion-usuarios/', views.activacion_usuarios, name='activacion-usuarios'),
    path('users/leads/', views.LeadsView.as_view(), name='leads'),
    path(r'users/', include(usersrouter.urls)),


]

if settings.DEBUG:
    urlpatterns += [
        path('iot/mock_lectura/', views.mock_lectura, name='mock_lectura'),
    ]
