import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
#from .captura import lectura

@csrf_exempt
def lectura(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            body = request.body
        print(body)
        if body['Type'] == 'SubscriptionConfirmation':
            requests.get(body['SubscribeURL'])
        #mensaje = lectura(body['Message'])
        return HttpResponse('post')
    else:
        return HttpResponse('get')