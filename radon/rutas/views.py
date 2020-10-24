from django.http import JsonResponse
from radon.rutas.models import Position
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def endpointgps(request):
    if request.method == 'GET':
        get = request.GET
        pos = Position.objects.create(location=f'POINT({get["lat"]} {get["lon"]})')
    elif request.method == 'POST':
        post = request.POST
        pos = Position.objects.create(location=f'POINT({post["lat"]} {post["lon"]})')
        return JsonResponse({'metodo': 'POST', 'contenido': 'Hola desde POST', 'pos': pos.location})


def last_pos(request):
    pos = Position.objects.all().order_by('-fecha_creacion').first()
    if pos:
        return JsonResponse({'lat': pos.location.x, 'lon': pos.location.y})
    return JsonResponse({'disps': 'todavia no tienes dispositivos'})
