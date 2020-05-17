from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path(r'', views.DashboardView.as_view(), name='inicio'),
    path(r'dispositivos/', views.DispositivoListView.as_view(), name='dispositivos'),
]
