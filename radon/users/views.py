from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse
from django.views.generic import (CreateView, ListView, DetailView, DeleteView, UpdateView)
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
