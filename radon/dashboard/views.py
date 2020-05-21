from django.urls import reverse
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, UpdateView,
    DeleteView, FormView)
from radon.users.auth import AuthenticationTestMixin
from radon.iot.models import Dispositivo
from radon.iot.forms import GeoForm

# Create your views here.


class DashboardView(TemplateView, AuthenticationTestMixin):
    template_name = "dashboard/index.html"


class DispositivoListView(ListView):
    paginate_by = 10
    model = Dispositivo
    template_name = "dashboard/dispositivo_list.html"

    def get_queryset(self):
        query = self.model.objects.filter(
            usuario__gasera=self.request.user.gasera
        )
        return query


class DispositivoDetailView(DetailView):
    model = Dispositivo
    template_name = "dashboard/dispositivo_detail.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            pk=self.kwargs['pk'],
            usuario__gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('dashboard:dispositivo_detail', kwargs={'pk': self.object.pk})


class DispositivoUpdateView(FormView):
    form_class = GeoForm
    template_name = "dashboard/dispositivo_update.html"


    def get_success_url(self):
        return reverse('dashboard:dispositivo_detail', kwargs={'pk': self.object.pk})


class DispositivoDeleteView(DeleteView):
    model = Dispositivo
    template_name = "dashboard/dispositivo_delete.html"

    def get_object(self, queryset=None):
        self.object = self.model.objects.get(
            pk=self.kwargs['pk'],
            usuario__gasera=self.request.user.gaserac
        )
        return self.object

    def get_success_url(self):
        return reverse('dashboard:dispositivo_list', kwargs={'pk': self.object.pk})

