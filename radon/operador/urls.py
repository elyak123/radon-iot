from django.urls import path, include
from radon.operador import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name="inicio"),
    path('creacion-usuario/', views.CreacionUsuarioView.as_view(), name="creacion-usuario"),
    path('checar-email/', views.ChecarEmailView, name="checar-email"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', include('radon.accounts.urls')),
    path('users/', include('radon.users.urls')),
    path('users/', include('radon.api.urls.usersurls'), name='usersapi'),
    path('iot/', include('radon.api.urls.ioturls')),
]
