from django.contrib.sites.models import Site

virtual_hosts = {
    "enterprise.radargas.com": "",
    "app.radargas.com": "",
    "logistica.radargas.com": "",
    "api.radargas.com": ""
}


class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # let's configure the root urlconf
        host = request.get_host()
        request.urlconf = virtual_hosts.get(host)
        # order matters!
        response = self.get_response(request)
        import pdb; pdb.set_trace()
        return response
