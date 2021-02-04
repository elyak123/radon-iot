from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('detalle/', views.UserDetailView.as_view(), name='user_detail'),
    path('editar/', views.UserUpdateView.as_view(), name='user_update'),
]
