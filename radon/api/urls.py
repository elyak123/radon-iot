from django.conf import settings
from django.urls import re_path, include, path
from rest_framework import routers
from radon.users import views as user_views
from radon.iot import views as iot_views

users_router = routers.DefaultRouter()
users_router.register(r'users', user_views.UserViewSet)
# iot_router = routers.DefaultRouter()
# iot_router.register(r'iot', iot_views.DeviceViewSet)

urlpatterns = [
    re_path(r'^v1/', include((users_router.urls, 'users'), namespace='v1')),
    #re_path(r'^v1/', include((iot_router.urls, 'iot'), namespace='v1')),
]
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]
