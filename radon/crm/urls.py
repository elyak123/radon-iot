from django.urls import path, re_path, include
from . import views

app_name = 'crm'

urlpatterns = [
    path(r'', views.DispositivoCriticoListView.as_view(), name='inicio'),
    path('', include('radon.accounts.urls')),
    re_path(r'^geojsons/(?P<fecha>\d{4}-\d{2}-\d{2})/$', views.get_geojsons, name="geojsons"),
    path('users/', include('radon.users.urls'), name="users"),
    path(r'dispositivos/', views.DispositivoListView.as_view(), name='dispositivo_list'),
    path(r'dispositivos/<int:serie>/', views.DispositivoDetailView.as_view(), name='dispositivo_detail'),
    path(r'dispositivos/eliminar/<int:serie>/', views.DispositivoDeleteView.as_view(), name='dispositivo_delete'),
    path(r'dispositivos/editar/<int:serie>/', views.DispositivoUpdateView.as_view(), name='dispositivo_update'),
    re_path(r'^pedidos/nuevo/(?P<dispositivo>\d+)/(?:(?P<week>\d{4}\-W\d{2})/)?$', views.PedidoCreateView.as_view(), name='pedido_creation'),
    re_path(r'^pedidos/(?:(?P<week>\d{4}\-W\d{2})/)?$', views.PedidoView.as_view(), name="histograma_pedidos"),
]
