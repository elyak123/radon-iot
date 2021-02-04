from django.conf import settings
from django_hosts.resolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import (
    LoginView, SignupView, PasswordChangeView,
    PasswordSetView, PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView, LogoutView, EmailVerificationSentView,
    AccountInactiveView, EmailView, ConfirmEmailView)
from radon.app.views import BaseTemplateSelector

User = get_user_model()


class BaseContext(object):
    def get_context_data(self, **kwargs):
        context = super(BaseContext, self).get_context_data(**kwargs)
        context['favicon'] = settings.FAVICON_URL
        context['template'] = 'account/base.html'
        return context


class _SignupView(BaseContext, SignupView):
    pass


class _LoginView(BaseContext, LoginView):
    def get_context_data(self, **kwargs):
        context = super(_LoginView, self).get_context_data(**kwargs)
        context['allow_register'] = settings.ACCOUNT_ALLOW_REGISTRATION
        context['subdominio'] = self.request.host.regex if not settings.ACCOUNT_ALLOW_REGISTRATION else None
        return context

    def get_success_url(self):
        return reverse('inicio', host=self.request.host.regex)


class _LogoutView(LoginRequiredMixin, BaseContext, LogoutView):
    pass


# original: BaseContext, AuthenticationTestMixin, PasswordChangeView
class _PasswordChangeView(BaseContext, PasswordChangeView, BaseTemplateSelector):
    pass


class _PasswordSetView(BaseContext, PasswordSetView, BaseTemplateSelector):
    pass


class _PasswordResetView(BaseContext, PasswordResetView, BaseTemplateSelector):
    pass


class _PasswordResetDoneView(BaseContext, PasswordResetDoneView, BaseTemplateSelector):
    pass


class _PasswordResetFromKeyView(BaseContext, PasswordResetFromKeyView, BaseTemplateSelector):
    pass


class _PasswordResetFromKeyDoneView(BaseContext, PasswordResetFromKeyDoneView, BaseTemplateSelector):
    pass


class _AccountInactiveView(BaseContext, AccountInactiveView, BaseTemplateSelector):
    pass


class _EmailView(BaseContext, EmailView, BaseTemplateSelector):
    pass


class _EmailVerificationSentView(BaseContext, EmailVerificationSentView, BaseTemplateSelector):
    pass


class _ConfirmEmailView(BaseContext, ConfirmEmailView):
    def get_redirect_url(self):
        return reverse('inicio', host=self.request.host.regex)
