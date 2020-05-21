from django.shortcuts import render
from django.views.generic import View

# Create your views here.

def PedidosDiaView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest("No funciona así.")

    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
