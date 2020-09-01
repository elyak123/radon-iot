from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import LoginView
from radon.users import views as userviews
from radon.iot import views as iotviews
from radon.api import serializers

###########################################
#  VIEWS AUTENTICACION Y AUTORIZACION API #
###########################################


class APIUsersLoginView(LoginView):
    permission_classes = ()
    authentication_classes = ()

    def get_response_serializer(self):
        return serializers.ExpirationJWTSerializer


class APIRefreshUsersView(TokenRefreshView):
    serializer_class = serializers.ExpirationRefreshJWTSerializer

####################
#  VIEWS PARA USER #
####################


class APILeadsView(userviews.LeadsView):
    pass


class APIUserViewSet(userviews.UserViewSet):
    pass


class APIRegisterUsersView(userviews.RegisterUsersView):
    pass


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # por lo pronto....
def api_activacion_usuarios(request):
    return userviews.activacion_usuarios(request)

####################
#  VIEWS PARA IOT #
####################


class APIDeviceTypeViewSet(iotviews.DeviceTypeViewSet):
    pass


class APIDeviceViewSet(iotviews.DeviceViewSet):
    pass


class APIInstalacionViewSet(iotviews.InstalacionViewSet):
    pass


class APIWisolViewSet(iotviews.WisolViewSet):
    pass


class APILecturaViewSet(iotviews.LecturaViewSet):
    pass


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # por lo pronto....
def api_wisol_initial_validation(request):
    return iotviews.wisol_initial_validation(request)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def api_registrolectura(request):
    return iotviews.registrolectura(request)


@api_view(['POST'])
def api_mock_lectura(request):
    return iotviews.mock_lectura(request)

@api_view(['POST'])
def api_mock_lecturas(request):
    return iotviews.mock_lecturas(request)
