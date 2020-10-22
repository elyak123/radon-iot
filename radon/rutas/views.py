from django.http import JsonResponse


def endpointgps(request):
    if request.method == 'GET':
        return JsonResponse({'metodo': 'GET', 'contenido': 'Hola desde GET'})
    return JsonResponse({'metodo': 'POST', 'contenido': 'Hola desde POST'})
