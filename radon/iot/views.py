import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import validate_aws_sns_message
# from .captura import lectura


@csrf_exempt
def lectura(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            validate_aws_sns_message.validate(body)
        except json.decoder.JSONDecodeError:
            body = request.body
        print(body)
        if body['Type'] == 'SubscriptionConfirmation':
            requests.get(body['SubscribeURL'])
        # angulo, temperatura, humedad = lectura(body['Message'])
        return HttpResponse('post')
    else:
        return HttpResponse('get')
