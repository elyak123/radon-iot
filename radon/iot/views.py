import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
import validate_aws_sns_message
from radon.iot.serializers import DispositivoSerializer, DeviceTypeSerializer
from radon.iot.models import Dispositivo, DeviceType
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


@api_view(['POST', 'GET'])
@permission_classes([permissions.AllowAny])
def lectura(request):
    if request.method == 'POST':
        # try:
        #     body = json.loads(request.body)
        #     validate_aws_sns_message.validate(body)
        # except validate_aws_sns_message.ValidationError:
        #     return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
        # if body['Type'] == 'SubscriptionConfirmation':
        #     requests.get(body['SubscribeURL'])
        # message = json.loads(body['Message'])
        # angulo, temperatura, humedad = sigfox_decode(message['data'])
        return JsonResponse({'cookie': request.COOKIES.get('mi_galleta', 'No hay cookie')}, status=200)
    else:
        response = JsonResponse({'get': True}, status=200)
        response.set_cookie('mi_galleta', value='comeme soy galleta', httponly=True)
        return response


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
