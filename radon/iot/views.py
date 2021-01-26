import json
import requests
import datetime
import pytz
from random import random
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework import status
import validate_aws_sns_message
from radon.iot import serializers, models, utils
from .captura import decode_int_little_endian


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
    # Checar si el sns viene de amazon.
    message_type = request.headers.get('x-amz-sns-message-type')
    aws_arn = request.headers.get('x-amz-sns-topic-arn')
    sns_types = ['SubscriptionConfirmation', 'Notification', 'UnsubscribeConfirmation']
    data = request.data
    if message_type not in sns_types or aws_arn != settings.SNS_SIGFOX_ARN:
        return HttpResponseBadRequest('<h1>400 Bad Request</h1>', content_type='text/html')
    #  Checar la validez del sns.
    try:
        body = json.loads(data)
        validate_aws_sns_message.validate(body)
    except validate_aws_sns_message.ValidationError as e:
        raise e
    # Veriricar si es un mensaje de suscripción
    if message_type == 'SubscriptionConfirmation':
        requests.get(body['SubscribeURL'])
        return HttpResponse('Suscripcion Realizada', status=200)
    # Realizar el registro de la lectura y el boletinado.
    message = json.loads(body['Message'])
    angulo = decode_int_little_endian(message['data'])
    dispositivo = get_object_or_404(models.Dispositivo, wisol__serie=message['device'])
    if angulo > 4095:
        dispositivo.status = "ROJO"
        porcentaje = dispositivo.get_ultima_lectura()['lectura']
    else:
        porcentaje = utils.convertir_lectura((int(angulo)*4095)/360, dispositivo.tipo)
    tz = pytz.timezone(settings.TIME_ZONE)
    models.Lectura.objects.create(
        fecha=tz.fromutc(datetime.datetime.utcnow()),
        porcentaje=porcentaje,
        dispositivo=dispositivo,
        sensor=angulo
    )
    return HttpResponse('Registro Creado', status=201)


def mock_lectura(request):
    disp = models.Dispositivo.objects.get(wisol__serie=request.data['dispositivo'])
    porcentaje = utils.convertir_lectura(int(request.data['sensor']))
    models.Lectura.objects.create(sensor=request.data['sensor'], porcentaje=porcentaje, dispositivo=disp)
    return HttpResponse('Registro Creado', status=201)


def mock_lecturas(request):
    disp = models.Dispositivo.objects.get(wisol__serie=request.data['dispositivo'])
    if not disp.lectura_set.last():
        inicial = 85 + round(random()*10, 2)
        hoy = datetime.datetime.now()
    else:
        inicial = disp.lectura_set.last().porcentaje
        hoy = disp.lectura_set.last().fecha
    delta = datetime.timedelta(days=0.5)
    registros = 5 + round(random()*20)
    for i in range(0, registros):
        if inicial < 0:
            inicial = 80 + round(random()*10, 2)
        models.Lectura.objects.create(porcentaje=inicial, sensor=utils.convertir_lectura(
            inicial, 1, 1), dispositivo=disp, fecha=hoy)
        inicial = float(inicial) - round(random()*3, 2)
        hoy = hoy + delta
    return HttpResponse(f'{registros} registros creados', status=201)


def registro_wisol(request):
    url = 'https://api.sigfox.com/v2/{}'
    creds = (settings.SIGFOX_CREDENTIAL_ID, settings.SIGFOX_CREDENTIAL_KEY)
    requests.post(
        url.format('devices/'),
        auth=creds,
        json={
            'name': '', 'deviceTypeId': '', 'id': '', 'pac': '', 'prototype': True
        }
    )
