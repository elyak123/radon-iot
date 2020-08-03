import json
import requests
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import validate_aws_sns_message
from radon.iot import serializers, models
from .captura import sigfox_decode


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceType.objects.all()
    serializer_class = serializers.DeviceTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Dispositivo.objects.all()
    serializer_class = serializers.DispositivoSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'wisol__serie'


class InstalacionViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.InstalacionSerializer
    permission_classes = [permissions.IsAuthenticated] # por lo pronto

    def get_queryset(self):
        return models.Instalacion.objects.filter(operario=self.request.user).order_by('-fecha')


class WisolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Wisol.objects.all()
    serializer_class = serializers.WisolSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'serie'


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated]) # por lo pronto....
def wisol_initial_validation(request):
    serializer = serializers.WisolValidation(data=request.data)
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
    dispositivo = models.Dispositivo.objects.get(wisol__serie=message['device'])
    models.Lectura.objects.create(nivel=porcentaje, dispositivo=dispositivo)
    return HttpResponse('Registro Creado', status=201)


@api_view(['POST'])
def mock_lectura(request):
    disp = models.Dispositivo.objects.get(wisol__serie=request.data['dispositivo'])
    models.Lectura.objects.create(nivel=request.data['nivel'], dispositivo=disp)
    return HttpResponse('Registro Creado', status=201)


def registro_wisol(request):
    url = 'https://api.sigfox.com/v2/{}'
    creds = (settings.SIGFOX_CREDENTIAL_ID, settings.SIGFOX_CREDENTIAL_KEY)
    r = requests.post(
            url.format('devices/'),
            auth=creds,
            json={
                'name': '', 'deviceTypeId': '', 'id': '', 'pac': '', 'prototype': True
            }
        )
