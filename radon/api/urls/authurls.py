from django.urls import path, include
from radon.api.views import APIUsersLoginView, APIRefreshUsersView

urlpatterns = [
    ################################
    #  URLS PARA AUTENTICACION API #
    ################################

    path('login/', APIUsersLoginView.as_view(), name='rest_login'),
    path('refresh/', APIRefreshUsersView.as_view(), name='token_refresh'),
    path('', include('dj_rest_auth.urls')),
]
