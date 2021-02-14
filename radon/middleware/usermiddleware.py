from django.utils.deprecation import MiddlewareMixin
from radon.users.models import Consumidor, Operador, Cliente, Staff, SuperUser

user_mapping = {
    'CONSUMIDOR': Consumidor,
    'OPERARIO': Operador,
    'CLIENTE': Cliente
}


def user_mapper(user):
    if user.tipo == 'STAFF':
        if user.is_superuser():
            user.__class__ = SuperUser
        else:
            user.__class__ = Staff
    else:
        user.__class__ = user_mapping[user.tipo]


class UserTypeMappingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            host = request.headers.get('HOST').split('.')[0]
        except AttributeError:
            host = request.environ['SERVER_NAME']  # solo para tests
        if host != 'api':
            if hasattr(request.user, 'tipo'):
                user_mapper(request.user)
