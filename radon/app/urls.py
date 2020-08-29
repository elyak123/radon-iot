from django.urls import path, include
from radon.app.views import DashboardView, GraphView, RegisterView, PedidoView
from radon.operador.views import ChecarEmailView


urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', include('radon.accounts.urls')),
    path('users/', include('radon.users.urls'), name="users"),
    path('users/', include('radon.api.urls.usersurls'), name='usersapi'),
    path('register/', RegisterView.as_view(), name="register"),
    path('pedido/', PedidoView.as_view(), name="pedido"),
    path('checar-email/', ChecarEmailView, name="checar-email"),
    path('iot/', include('radon.api.urls.ioturls')),
    path('auth/', include('radon.api.urls.authurls')),
    path("consumo/", GraphView.as_view(), name="grafica")
]
