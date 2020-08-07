from django.urls import path, include, re_path
from radon.users.views import UsersLoginView, RefreshUsersView
from radon.operador import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name="inicio"),
    path('creacion-usuario/', views.CreacionUsuarioView.as_view(), name="creacion-usuario"),
    path('checar-email/', views.ChecarEmailView, name="checar-email"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', include('radon.accounts.urls')),
    path('iot/', include('radon.iot.urls')),
    path('users/', include('radon.users.urls')),
    re_path(r'^auth/login/$', UsersLoginView.as_view(), name='rest_login'),
    re_path(r'^auth/refresh/$', RefreshUsersView.as_view(), name='token_refresh'),
    re_path(r'^auth/', include('dj_rest_auth.urls')),
]
