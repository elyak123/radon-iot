from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "www/index.html"


class PreguntasView(generic.TemplateView):
    template_name = "www/preguntas.html"
