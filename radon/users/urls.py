from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)
from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'token-verify/', TokenVerifyView.as_view()),
]
