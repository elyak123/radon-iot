import json
import requests
import datetime
from random import random
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import status
import validate_aws_sns_message
from radon.iot import serializers, models, utils
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
    permission_classes = [permissions.AllowAny]
    lookup_field = 'wisol__serie'


class InstalacionViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.InstalacionSerializer
    permission_classes = [permissions.IsAuthenticated]  # por lo pronto

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


class LecturaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LecturaSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return models.Lectura.objects.filter(
                dispositivo__wisol__serie=self.request.GET['dispositivo']
            ).order_by('-fecha')
        except KeyError:
            return models.Lectura.objects.filter(
                dispositivo__usuario__gasera=self.request.user.gasera).order_by('-fecha')


def wisol_initial_validation(request):
    serializer = serializers.WisolValidation(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'wisol': 'valid'}, status.HTTP_200_OK, {})


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


def mock_lectura(request):
    disp = models.Dispositivo.objects.get(wisol__serie=request.data['dispositivo'])
    porcentaje = utils.convertir_lectura(int(request.data['sensor']))
    models.Lectura.objects.create(sensor=request.data['sensor'], porcentaje=porcentaje, dispositivo=disp)
    return HttpResponse('Registro Creado', status=201)


def mock_lecturas(request):
    disp = models.Dispositivo.objects.get(wisol__serie=request.data['dispositivo'])
    inicial = 80 + round(random()*10, 2)
    hoy = datetime.datetime.now()
    delta = datetime.timedelta(days=0.5)
    registros = round(random()*100)
    for i in range(0, registros):
        if inicial < 0:
            inicial = 80 + round(random()*10, 2)
        models.Lectura.objects.create(porcentaje=inicial, sensor=utils.convertir_lectura(inicial, 1, 1), dispositivo=disp, fecha=hoy)
        inicial = inicial - round(random()*3, 2)
        hoy = hoy + delta
    return HttpResponse(f'{registros} registros creados', status=201)


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
