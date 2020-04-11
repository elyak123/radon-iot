import json
import requests
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
import validate_aws_sns_message
from radon.iot.serializers import DispositivoSerializer, DeviceTypeSerializer
from radon.iot.models import Dispositivo, DeviceType, Lectura
from .captura import sigfox_decode


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer
    permission_classes = [permissions.IsAdminUser]


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
    dispositivo = Dispositivo.get(serie=message['device'])
    Lectura.objects.create(nivel=porcentaje, dispositivo=dispositivo)
    return HttpResponse('Registro Creado', status_code=201)


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
