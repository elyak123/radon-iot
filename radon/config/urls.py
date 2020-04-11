"""radon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView
from radon.users.views import UsersLoginView


urlpatterns = [
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            TemplateView.as_view(template_name="account/password_reset_confirm.html"),
            name='password_reset_confirm'),
    re_path(r'^auth/login/$', UsersLoginView.as_view(), name='rest_login'),
    re_path(r'^auth/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^auth/', include('dj_rest_auth.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('radon.users.urls')),
    path('iot/', include('radon.iot.urls')),
]
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
