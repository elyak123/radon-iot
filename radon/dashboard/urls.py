from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path(r'', views.DashboardView.as_view(), name='inicio'),
    path(r'dispositivos/', views.DispositivoListView.as_view(), name='dispositivo_list'),
    path(r'dispositivos/<pk>', views.DispositivoDetailView.as_view(), name='dispositivo_detail'),
    path(r'dispositivos/eliminar/<pk>', views.DispositivoDeleteView.as_view(), name='dispositivo_delete'),
    path(r'dispositivos/editar/<pk>', views.DispositivoUpdateView.as_view(), name='dispositivo_update'),
]
