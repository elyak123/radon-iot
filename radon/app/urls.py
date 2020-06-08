from django.urls import path, include
from radon.app.views import IndexView

urlpatterns = [
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('inicio/', IndexView.as_view(), name="inicio")
]
