from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from dj_rest_auth.registration.views import RegisterView
from django.views.generic import (
    CreateView, ListView, DetailView, DeleteView,
    UpdateView)
from radon.users import serializers
from radon.users import forms as uf
from radon.users.auth import AuthenticationTestMixin
from radon.app.views import BaseTemplateSelector


User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('location')
)


class UserCreateView(CreateView, AuthenticationTestMixin, BaseTemplateSelector):
    form_class = uf.UserForm
    model = User
    template_name = "users/user_create.html"

    def form_valid(self, form):
        form.instance.gasera = self.request.user.gasera
        form.instance.pwdtemporal = False
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:inicio')


class UserListView(ListView, AuthenticationTestMixin, BaseTemplateSelector):
    paginate_by = 10
    model = User
    template_name = "users/user_list.html"

    def get_queryset(self):
        query = self.model.objects.filter(
            gasera=self.request.user.gasera
        )
        return query


class UserDetailView(DetailView, BaseTemplateSelector):
    model = User
    template_name = "users/user_detail.html"

    def get_object(self, queryset=None):
        self.object = User.objects.get(
            username=self.kwargs['username'],
            gasera=self.request.user.gasera
        )
        return self.object


class UserDeleteView(DeleteView, BaseTemplateSelector):
    model = User
    template_name = "users/user_delete.html"

    def get_object(self, queryset=None):
        self.object = User.objects.get(
            username=self.kwargs['username'],
            gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('users:user_list')


class UserUpdateView(UpdateView, BaseTemplateSelector):
    model = User
    template_name = "users/user_update.html"
    form_class = uf.UserUpdateForm

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.object
        return kwargs

    def get_object(self, queryset=None):
        self.object = User.objects.get(
            username=self.kwargs['username'],
            gasera=self.request.user.gasera
        )
        return self.object

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'username': self.object.username})


class LeadsView(ListAPIView):
    serializer_class = serializers.LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.especial.leads(self.request.user.gasera).order_by('ultima_lectura')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class RegisterUsersView(RegisterView):
    serializer_class = serializers.TemporalPassUserDispsitivoCreation
    permission_classes = [permissions.AllowAny]  # por lo pronto....

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(RegisterView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user


def activacion_usuarios(request):
    serializer = serializers.ActivateUsers(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK, {})
