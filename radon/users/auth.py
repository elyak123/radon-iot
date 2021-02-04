from django.contrib.auth.mixins import UserPassesTestMixin
from radon.users.models import Consumidor, Operador, Cliente, Staff, SuperUser


class AuthenticationTestMixin(UserPassesTestMixin):

    def test_func(self):
        if not hasattr(self, 'user_class'):
            raise NotImplementedError('Es necesario el path para la clase del tipo de usuario')
        return isinstance(self.request.user, self.user_class)


class ConsumidorAutenticationMixin(AuthenticationTestMixin):
    user_class = Consumidor


class SatffAutenticationMixin(AuthenticationTestMixin):
    user_class = Staff


class OperadorAutenticationMixin(AuthenticationTestMixin):
    user_class = Operador


class ClienteAutenticationMixin(AuthenticationTestMixin):
    user_class = Cliente


class SuperUsuarioAutenticationMixin(AuthenticationTestMixin):
    user_class = SuperUser
