from django.urls import path, include
from radon.app.views import DashboardView

urlpatterns = [
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('inicio/', DashboardView.as_view(), name="inicio")
]
