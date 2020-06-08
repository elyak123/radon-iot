from django.contrib.sites.models import Site
from django.http import Http404
from radon.siteprofile.models import Sitio


class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # let's configure the root urlconf
        host = request.get_host().split(":")[0]
        try:
            sitio = Sitio.objects.get(domain=host)
            request.urlconf = sitio.modulo
        except Sitio.DoesNotExist:
            raise Http404("El sitio al que está tratando de acceder no existe.")
        # order matters!
        response = self.get_response(request)
        return response
