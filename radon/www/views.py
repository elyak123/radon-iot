from django.views import generic
import random


class IndexView(generic.TemplateView):
    template_name = "www/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['aleatorio'] = random.randint(1, 4)
        return context


class PreguntasView(generic.TemplateView):
    template_name = "www/preguntas.html"

    def get_context_data(self, **kwargs):
        context = super(PreguntasView, self).get_context_data(**kwargs)
        context['aleatorio'] = random.randint(1, 4)
        return context
