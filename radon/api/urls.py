from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import routers
from .views import APIUsersLoginView, APIRefreshUsersView
from . import views

app_name = 'api'

#####################
#  ROUTER PARA USER #
#####################
usersrouter = routers.DefaultRouter()
usersrouter.register(r'', views.APIUserViewSet, basename='user')

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
    path('iot/registro-lectura/', views.api_registrolectura, name='registrolectura'),
    path('iot/disponibilidad-wisol/', views.api_wisol_initial_validation, name='dispwisol'),
    path(r'iot/', include(iotrouter.urls)),

    ####################
    #  URLS PARA USERS #
    ####################
    path('users/user-dispositivo-registration/', views.APIRegisterUsersView.as_view(), name='usr-disp-reg'),
    path('users/activacion-usuarios/', views.api_activacion_usuarios, name='activacion-usuarios'),
    path('users/leads/', views.APILeadsView.as_view(), name='leads'),
    path(r'users/', include(usersrouter.urls)),


    ################################
    #  URLS PARA AUTENTICACION API #
    ################################
    re_path(r'^auth/login/$', APIUsersLoginView.as_view(), name='rest_login'),
    re_path(r'^auth/refresh/$', APIRefreshUsersView.as_view(), name='token_refresh'),
    re_path(r'^auth/', include('dj_rest_auth.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        path('iot/mock_lectura/', views.api_mock_lectura, name='mock_lectura'),
    ]
