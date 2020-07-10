from django.urls import path, include
from radon.app.views import DashboardView, GraphView


urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', DashboardView.as_view(), name="inicio"),
    path("comsumo/", GraphView.as_view(), name="grafica")
]
