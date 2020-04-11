from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from dj_rest_auth.views import LoginView
from radon.users.serializers import UserSerializer, ExpirationJWTSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self, request):
        return User.objects.all().order_by('-date_joined')


class UsersLoginView(LoginView):

    def get_response_serializer(self):
        return ExpirationJWTSerializer
