from django.urls import path, include
from radon.api import views
from rest_framework import routers

#####################
#  ROUTER PARA USER #
#####################
usersrouter = routers.DefaultRouter()
usersrouter.register(r'', views.APIUserViewSet, basename='user')

urlpatterns = [

    ####################
    #  URLS PARA USERS #
    ####################
    path('user-dispositivo-registration/', views.APIRegisterUsersView.as_view(), name='usr-disp-reg'),
    path('activacion-usuarios/', views.api_activacion_usuarios, name='activacion-usuarios'),
    path('leads/', views.APILeadsView.as_view(), name='leads'),
    path(r'', include(usersrouter.urls)),
]
