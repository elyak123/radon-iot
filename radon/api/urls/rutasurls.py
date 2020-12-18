from django.urls import path, include
from radon.api import views
from rest_framework import routers


rutasrouter = routers.DefaultRouter()
rutasrouter.register(r'pedido', views.APIPedidoViewSet, basename='pedido')

urlpatterns = [

    ####################
    #  URLS PARA RUTAS #
    ####################
    path(r'', include(rutasrouter.urls)),
]
