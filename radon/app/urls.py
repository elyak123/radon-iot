from django.urls import path, include
from radon.app.views import DashboardView, sigfox

urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('sigfox/', sigfox),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
]
