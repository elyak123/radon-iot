from django.urls import path
from django.conf import settings
from radon.iot import views

app_name = 'iot'

urlpatterns = [
    path('sns-lectura-registro/', views.registrolectura, name='sns-lectura-registro'),
]

if settings.DEBUG:
    urlpatterns += [

    ]
