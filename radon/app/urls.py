from django.urls import path, re_path, include
from radon.app.views import (DashboardView, GraphView, RegisterView,
                             PedidoView, PedidosView, PedidoDetailView, DispositivoDetailView,
                             asset_links, RegistroDispositivo)
from radon.operador.views import ChecarEmailView


urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', include('radon.accounts.urls')),
    path('users/', include('radon.users.urls'), name="users"),
    path('users/', include('radon.api.urls.usersurls'), name='usersapi'),
    path('register/', RegisterView.as_view(), name="register"),
    path(r'pedido/<slug:serie>/', PedidoView.as_view(), name="pedido"),
    path(r'dispositivos/<slug:serie>/', DispositivoDetailView.as_view(), name='dispositivo_detail'),
    path('pedidos/', PedidosView.as_view(), name="pedidos"),
    re_path(r'^pedido/detalle/(?P<pk>\d+)/?$', PedidoDetailView.as_view(), name='detalle-pedido'),
    path('checar-email/', ChecarEmailView, name="checar-email"),
    path('registrar/', RegistroDispositivo.as_view(), name="nuevo_dispositivo"),
    path('iot/', include('radon.api.urls.ioturls')),
    path('auth/', include('radon.api.urls.authurls')),
    path('.well-known/assetlinks.json', asset_links, name="assetlinks"),
    path(r'consumo/<slug:serie>/', GraphView.as_view(), name="grafica")
]
