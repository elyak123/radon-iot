from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def lectura(request):
    if request.method == 'POST':
        print(request)
        print(request.POST)
        print(request.body)
        print(request.headers)
        return HttpResponse('post')
    else:
        return HttpResponse('get')