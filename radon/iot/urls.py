from django.urls import path
from . import views

app_name = 'iot'

urlpatterns = [
    path('lectura/', views.lectura, name='lectura'),
]