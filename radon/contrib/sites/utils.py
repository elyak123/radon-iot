from django.conf import settings
from django_hosts.resolvers import get_host_patterns
from django.contrib.sites.models import Site


def create_sites():
    for host in get_host_patterns():
        domain = f'{host.regex}.{settings.PARENT_HOST}'
        try:
            Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            Site.objects.create(domain=domain, name=domain)
