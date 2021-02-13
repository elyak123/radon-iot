from dj_rest_auth.utils import JWTCookieAuthentication
from radon.middleware.usermiddleware import user_mapper


class UserClassificationJWTCookieAuthentication(JWTCookieAuthentication):
    def authenticate(self, request):
        try:
            user, validated_token = super(UserClassificationJWTCookieAuthentication, self).authenticate(request)
        except TypeError:
            return None
        user_mapper(user)
        return user, validated_token
