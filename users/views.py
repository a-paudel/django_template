from typing import Any
from django.contrib.auth.views import (
    LoginView as _DjangoLoginView,
    LogoutView as _DjangoLogoutView,
    PasswordResetView as _DjangoPasswordResetView,
    PasswordResetDoneView as _DjangoPasswordResetDoneView,
    PasswordResetConfirmView as _DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as _DjangoPasswordResetCompleteView,
)

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView
from config import settings
from users.forms import LoginForm, PasswordResetForm, PasswordSetForm, RegisterForm

# Create your views here.


class LoginView(_DjangoLoginView):
    form_class = LoginForm
    template_name = "users/login.html"


class LogoutView(_DjangoLogoutView):
    pass


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not settings.ALLOW_REGISTRATION:
            return HttpResponseNotFound()
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not settings.ALLOW_REGISTRATION:
            return HttpResponseNotFound()
        return super().post(request, *args, **kwargs)


class PasswordResetView(_DjangoPasswordResetView):
    template_name = "users/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:password_reset_email_sent")
    subject_template_name = "users/emails/password_reset_subject.txt"
    email_template_name = "users/emails/password_reset_email.html"
    html_email_template_name = "users/emails/password_reset_email.html"


class PasswordResetEmailSentView(_DjangoPasswordResetDoneView):
    template_name = "users/password_reset_email_sent.html"


class PasswordResetConfirmView(_DjangoPasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    form_class = PasswordSetForm
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(_DjangoPasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
