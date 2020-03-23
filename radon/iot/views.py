import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
import validate_aws_sns_message
from radon.iot.serializers import DispositivoSerializer
from radon.iot.models import Dispositivo
from .captura import sigfox_decode


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dispositivo.objects.all().order_by('-date_joined')
    serializer_class = DispositivoSerializer
    permission_classes = [permissions.IsAdminUser]


@csrf_exempt
def lectura(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            validate_aws_sns_message.validate(body)
        except validate_aws_sns_message.ValidationError:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
        if body['Type'] == 'SubscriptionConfirmation':
            requests.get(body['SubscribeURL'])
        message = json.loads(body['Message'])
        angulo, temperatura, humedad = sigfox_decode(message['data'])
        return HttpResponse('post')
    else:
        return HttpResponse('get')


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
