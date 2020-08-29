from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from radon.users import views as userviews
from radon.iot import views as iotviews

####################
#  VIEWS PARA USER #
####################


class APILeadsView(userviews.LeadsView):
    pass


class APIUserViewSet(userviews.UserViewSet):
    pass


class APIUsersLoginView(userviews.UsersLoginView):
    pass


class APIRefreshUsersView(userviews.RefreshUsersView):
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
