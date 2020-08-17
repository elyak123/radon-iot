from django.urls import path, include, re_path
from radon.users.views import UsersLoginView, RefreshUsersView
from radon.app.views import DashboardView, GraphView
from radon.users.views import UserUpdateView


urlpatterns = [
    path('', DashboardView.as_view(), name="inicio"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('users/', include('radon.users.urls'), name="users"),
    path('dashboard/', include('radon.dashboard.urls'), name="dashboard"),
    re_path(r'^auth/login/$', UsersLoginView.as_view(), name='rest_login'),
    re_path(r'^auth/refresh/$', RefreshUsersView.as_view(), name='token_refresh'),
    re_path(r'^auth/', include('dj_rest_auth.urls')),
    path('', include('radon.accounts.urls')),
    path("consumo/", GraphView.as_view(), name="grafica")
]
