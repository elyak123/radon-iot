from django.urls import path, include
from radon.app.views import DashboardView, GraphView


urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('users/', include('radon.users.urls'), name="users"),
    path('', include('radon.accounts.urls')),
    path("consumo/", GraphView.as_view(), name="grafica")
]
