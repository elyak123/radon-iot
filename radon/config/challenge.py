from django.conf import settings
from django.http import HttpResponse

def acmechallenge(request):
    return HttpResponse(settings.ACME_CHALLENGE_CONTENT)