from django.urls import path
from . import views

app_name = 'www'

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='inicio'),
    path('preguntas-frecuentes/', views.PreguntasView.as_view(), name='preguntas'),
]
