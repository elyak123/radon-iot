from django.http import JsonResponse
from radon.rutas.models import Position
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def endpointgps(request):
    if request.method == 'GET':
        return JsonResponse({'metodo': 'GET', 'contenido': 'Hola desde GET'})
    elif request.method == 'POST':
        pos = Position.objects.create(location=f'POINT{request.POST["lat"]} {request.POST["lon"]}')
        return JsonResponse({'metodo': 'POST', 'contenido': 'Hola desde POST', 'pos': pos.location})


def last_pos(request):
    pos = Position.objects.all().order_by('-fecha_creacion').first()
    if pos:
        return JsonResponse({'lat': pos.location.x, 'lon': pos.location.y})
    return JsonResponse({'disps': 'todavia no tienes dispositivos'})
