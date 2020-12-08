from django.urls import path, include
from radon.api import views
from rest_framework import routers

#######################
#  ROUTER PARA MARKET #
#######################
marketrouter = routers.DefaultRouter()
marketrouter.register(r'gasera', views.APIGaseraViewSet, basename='gasera')
marketrouter.register(r'sucursal', views.APIGaseraViewSet, basename='sucursal')
marketrouter.register(r'precio', views.APIGaseraViewSet, basename='precio')

urlpatterns = [

    #####################
    #  URLS PARA MARKET #
    #####################
    path(r'', include(marketrouter.urls)),
]
