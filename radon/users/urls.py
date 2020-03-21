from django.urls import path
from rest_framework import routers
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserViewSet, name='users'),
]
