from django.utils.deprecation import MiddlewareMixin
from radon.users.models import Consumidor, Operador, Cliente, Staff, SuperUser


class UserTypeMappingMiddleware(MiddlewareMixin):
    user_mapping = {
        'CONSUMIDOR': Consumidor,
        'OPERARIO': Operador,
        'CLIENTE': Cliente
    }

    def process_request(self, request):
        if hasattr(request.user, 'tipo'):
            if request.user.tipo == 'STAFF':
                if request.user.is_superuser():
                    request.user.__class__ = SuperUser
                else:
                    request.user.__class__ = Staff
            else:
                request.user.__class__ = self.user_mapping[request.user.tipo]
