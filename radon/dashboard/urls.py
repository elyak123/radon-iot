from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'dashboard'

urlpatterns = [
    path(r'', views.DashboardView.as_view(), name='inicio'),
]
