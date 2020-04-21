from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
from radon.users import serializers

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('location')
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class UsersLoginView(LoginView):
    permission_classes = ()
    authentication_classes = ()

    def get_response_serializer(self):
        return serializers.ExpirationJWTSerializer


class RefreshUsersView(TokenRefreshView):
    serializer_class = serializers.ExpirationRefreshJWTSerializer


class RegisterUsersView(RegisterView):
    serializer_class = serializers.AsistedUserDispositivoCreation
    permission_classes = [permissions.IsAdminUser]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(RegisterView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user
