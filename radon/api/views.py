import json
import requests
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView
import validate_aws_sns_message
from radon.users import serializers as userserializers
from radon.iot import models as iotmodels
from radon.iot import serializers as iotserializers
from radon.iot.captura import sigfox_decode

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('location')
)

####################
#  VIEWS PARA USER #
####################


class LeadsView(ListAPIView):
    serializer_class = userserializers.LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.especial.leads(self.request.user.gasera).order_by('ultima_lectura')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = userserializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class UsersLoginView(LoginView):
    permission_classes = ()
    authentication_classes = ()

    def get_response_serializer(self):
        return userserializers.ExpirationJWTSerializer


class RefreshUsersView(TokenRefreshView):
    serializer_class = userserializers.ExpirationRefreshJWTSerializer


class RegisterUsersView(RegisterView):
    serializer_class = userserializers.TemporalPassUserDispsitivoCreation
    permission_classes = [permissions.IsAuthenticated]  # por lo pronto....

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(RegisterView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # por lo pronto....
def activacion_usuarios(request):
    serializer = userserializers.ActivateUsers(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK, {})

####################
#  VIEWS PARA IOT #
####################


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = iotmodels.DeviceType.objects.all()
    serializer_class = iotserializers.DeviceTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = iotmodels.Dispositivo.objects.all()
    serializer_class = iotserializers.DispositivoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'wisol__serie'


class InstalacionViewSet(viewsets.ModelViewSet):

    serializer_class = iotserializers.InstalacionSerializer
    permission_classes = [permissions.IsAuthenticated]  # por lo pronto

    def get_queryset(self):
        return iotmodels.Instalacion.objects.filter(operario=self.request.user).order_by('-fecha')


class WisolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = iotmodels.Wisol.objects.all()
    serializer_class = iotserializers.WisolSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'serie'


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # por lo pronto....
def wisol_initial_validation(request):
    serializer = iotserializers.WisolValidation(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'wisol': 'valid'}, status.HTTP_200_OK, {})


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def registrolectura(request):
    try:
        body = json.loads(request.body)
        validate_aws_sns_message.validate(body)
    except validate_aws_sns_message.ValidationError:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    if body['Type'] == 'SubscriptionConfirmation':
        requests.get(body['SubscribeURL'])
    message = json.loads(body['Message'])
    angulo, temperatura, humedad = sigfox_decode(message['data'])
    porcentaje = (angulo * 100) / 360
    dispositivo = iotmodels.Dispositivo.objects.get(wisol__serie=message['device'])
    iotmodels.Lectura.objects.create(nivel=porcentaje, dispositivo=dispositivo)
    return HttpResponse('Registro Creado', status=201)


@api_view(['POST'])
def mock_lectura(request):
    disp = iotmodels.Dispositivo.objects.get(wisol__serie=request.data['dispositivo'])
    iotmodels.Lectura.objects.create(nivel=request.data['nivel'], dispositivo=disp)
    return HttpResponse('Registro Creado', status=201)
