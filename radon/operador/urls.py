from django.urls import path, include
from radon.operador.views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', include('radon.accounts.urls')),
]
