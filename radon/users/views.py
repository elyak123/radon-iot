from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from radon.users.serializers import UserSerializer, ExpirationJWTSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UsersLoginView(LoginView):

    def get_response_serializer(self):
        return ExpirationJWTSerializer
