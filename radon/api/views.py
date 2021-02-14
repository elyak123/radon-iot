from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions as drf_permissions
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import parser_classes
from dj_rest_auth.views import LoginView
from radon.users import views as userviews
from radon.iot import views as iotviews
from radon.market import views as marketviews
from radon.rutas import views as rutasviews
from radon.georadon import views as geoviews
from radon.api import serializers, parsers, permissions

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
    permission_classes = [permissions.APIClientePermission | drf_permissions.IsAdminUser]


class APIUserViewSet(userviews.UserViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


class APIRegisterUsersView(userviews.RegisterUsersView):
    permission_classes = [drf_permissions.AllowAny]


@api_view(['POST'])
@permission_classes([drf_permissions.IsAuthenticated])
def api_activacion_usuarios(request):
    return userviews.activacion_usuarios(request)

#####################
#  VIEWS PARA RUTAS #
#####################


class APIPedidoViewSet(rutasviews.PedidoViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


######################
#  VIEWS PARA MARKET #
######################


class APIGaseraViewSet(marketviews.GaseraViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


class APISucursalViewSet(marketviews.SucursalViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


class APIPreciosViewSet(marketviews.PreciosViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


########################
#  VIEWS PARA GEORADON #
########################

@api_view(['GET'])
@permission_classes([drf_permissions.IsAdminUser])
def localidades_dispositivos(request):
    return geoviews.localidades_dispositivos(request)


####################
#  VIEWS PARA IOT #
####################


class APIDeviceTypeViewSet(iotviews.DeviceTypeViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


class APIDeviceViewSet(iotviews.DeviceViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


class APIInstalacionViewSet(iotviews.InstalacionViewSet):
    permission_classes = [permissions.APIOperadorPermission | drf_permissions.IsAdminUser]


class APIWisolViewSet(iotviews.WisolViewSet):
    permission_classes = [drf_permissions.IsAdminUser]


class APILecturaViewSet(iotviews.LecturaViewSet):
    permission_classes = [
        drf_permissions.IsAdminUser |
        permissions.APIConsumidorPermission |
        permissions.APIClientePermission]


@api_view(['POST'])
@permission_classes([drf_permissions.AllowAny])  # por lo pronto....
def api_wisol_initial_validation(request):
    return iotviews.wisol_initial_validation(request)


@api_view(['POST'])
@parser_classes([parsers.PlainTextParser])
@permission_classes([drf_permissions.AllowAny])
def api_registrolectura(request):
    return iotviews.registrolectura(request)


@api_view(['POST'])
def api_mock_lectura(request):
    return iotviews.mock_lectura(request)


@api_view(['POST'])
def api_mock_lecturas(request):
    return iotviews.mock_lecturas(request)
