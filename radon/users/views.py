from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from dj_rest_auth.registration.views import RegisterView
from radon.users import serializers
from radon.users import forms as uf
from radon.users.models import Cliente


User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('location')
)


class BaseTemplate(object):
    def get_context_data(self, **kwargs):
        context = super(BaseTemplate, self).get_context_data(**kwargs)
        context['favicon'] = settings.FAVICON_URL
        context['template'] = f'{self.request.host.regex}/base.html'
        return context


class UserDetailView(BaseTemplate, LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(BaseTemplate, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/user_update.html"
    form_class = uf.UserUpdateForm

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.object
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user_detail')


class LeadsView(ListAPIView):
    """
    Se llama desde API, sirve para obtener los leads desde CRM 'posiblemente'
    """
    serializer_class = serializers.LeadSerializer

    def get_queryset(self):
        return Cliente.objects.leads(self.request.user.sucursal).order_by('ultima_lectura')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'

    def get_queryset(self):
        if self.request.user.tipo == 'CONSUMIDOR':
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.all().order_by('-date_joined')


class RegisterUsersView(RegisterView):
    """
    Se llama desde API permite la creacion de Consumidores por medio de
    app y operador
    """
    serializer_class = serializers.TemporalPassUserDispsitivoCreation

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(RegisterView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user


def activacion_usuarios(request):
    """
    Se llama desde API, permite la activacion de consumidores
    """
    serializer = serializers.ActivateUsers(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK, {})
