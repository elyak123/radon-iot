from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'accounts'

urlpatterns = [
    path(r'signup/', views._SignupView.as_view(), name='account_signup'),
    path(r'login/', views._LoginView.as_view(), name='account_login'),
    path(r'logout/', views._LogoutView.as_view(), name='account_logout'),

    path(r'password/change/(?:(<username>[\w.@+-]+)/)?', views._PasswordChangeView.as_view(),
         name='account_change_password'),
    path(r'password/set/', views._PasswordSetView.as_view(), name='account_set_password'),

    path(r'inactive/', views._AccountInactiveView.as_view(), name='account_inactive'),

    # E-mail
    path(r'email/', views._EmailView.as_view(), name='account_email'),
    path(r'confirm-email/', views._EmailVerificationSentView.as_view(),
         name='account_email_verification_sent'),
    path(r'confirm-email/(<key>[-:\w]+)/', views._ConfirmEmailView.as_view(),
         name='account_confirm_email'),

    # password reset
    path(r'password/reset/', views._PasswordResetView.as_view(),
         name='account_reset_password'),
    path(r'password/reset/done/', views._PasswordResetDoneView.as_view(),
         name='account_reset_password_done'),
    path(r'password/reset/key/(<uidb36>[0-9A-Za-z]+)-(<key>.+)/',
         views._PasswordResetFromKeyView.as_view(),
         name='account_reset_password_from_key'),
    path(r'password/reset/key/done/', views._PasswordResetFromKeyDoneView.as_view(),
         name='account_reset_password_from_key_done'),
]
