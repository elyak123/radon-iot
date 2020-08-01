from django.urls import path, include, re_path
from radon.operador import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name="inicio"),
    path('creacion-usuario/', views.CreacionUsuarioView.as_view(), name="creacion-usuario"),
    path('checar-email/', views.ChecarEmailView, name="checar-email"),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('', include('radon.accounts.urls')),
    re_path(r'^auth/', include('dj_rest_auth.urls'))
]
