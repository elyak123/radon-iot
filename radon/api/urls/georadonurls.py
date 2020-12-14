from django.urls import path
from radon.api import views

urlpatterns = [
    path('localidades/dispositivos/', views.localidades_dispositivos),
]
