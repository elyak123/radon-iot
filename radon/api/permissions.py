from rest_framework.permissions import BasePermission
from radon.users.models import Consumidor, Cliente, Operador, Staff, SuperUser


class BaseRadonAPIPermission(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, self.user_class)


class APIConsumidorPermission(BaseRadonAPIPermission):
    user_class = Consumidor


class APIClientePermission(BaseRadonAPIPermission):
    user_class = Cliente


class APIOperadorPermission(BaseRadonAPIPermission):
    user_class = Operador


class APIStaffPermission(BaseRadonAPIPermission):
    user_class = (Staff, SuperUser)


class APISuperUserPermission(BaseRadonAPIPermission):
    user_class = SuperUser
