from django.urls import path, re_path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path(r'', views.DashboardView.as_view(), name='inicio'),
    path(r'dispositivos/', views.DispositivoListView.as_view(), name='dispositivo_list'),
    path(r'dispositivos/<int:pk>/', views.DispositivoDetailView.as_view(), name='dispositivo_detail'),
    path(r'dispositivos/eliminar/<int:pk>/', views.DispositivoDeleteView.as_view(), name='dispositivo_delete'),
    path(r'dispositivos/editar/<int:pk>/', views.DispositivoUpdateView.as_view(), name='dispositivo_update'),
    re_path(r'^pedidos/nuevo/(?P<dispositivo>\d+)/(?:(?P<week>\d+)/)?$', views.PedidoCreateView.as_view(), name='pedido_creation'),
    re_path(r'^pedidos/(?:(?P<week>\d+)/)?$', views.PedidoView.as_view(), name="histograma_pedidos"),
]
