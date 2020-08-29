from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('detalle/<username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('editar/<username>/', views.UserUpdateView.as_view(), name='user_update'),
    path('eliminar/<username>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('nuevo/', views.UserCreateView.as_view(), name='user_creation'),
]
