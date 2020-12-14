from django.urls import path, include
from radon.api import views
from rest_framework import routers

#######################
#  ROUTER PARA MARKET #
#######################
marketrouter = routers.DefaultRouter()
marketrouter.register(r'gasera', views.APIGaseraViewSet, basename='gasera')
marketrouter.register(r'sucursal', views.APISucursalViewSet, basename='sucursal')
marketrouter.register(r'precios', views.APIPreciosViewSet, basename='precio')

urlpatterns = [

    #####################
    #  URLS PARA MARKET #
    #####################
    path(r'', include(marketrouter.urls)),
]
