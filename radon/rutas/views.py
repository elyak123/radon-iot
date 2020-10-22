from django.http import JsonResponse


def endpointgps(request):
    if request.method == 'GET':
        JsonResponse({'metodo': 'GET', 'contenido': 'Hola desde GET'})
    elif request.method == 'POST':
        JsonResponse({'metodo': 'POST', 'contenido': 'Hola desde POST'})
