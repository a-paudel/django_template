from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView as _DjangoLoginView,
    LogoutView as _DjangoLogoutView,
    PasswordResetView as _DjangoPasswordResetView,
    PasswordResetDoneView as _DjangoPasswordResetDoneView,
    PasswordResetConfirmView as _DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as _DjangoPasswordResetCompleteView,
)
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginForm, PasswordResetForm, PasswordSetForm, RegisterForm
from users.models import User

# Create your views here.


class LoginView(_DjangoLoginView):
    form_class = LoginForm
    template_name = "users/login.html"

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        next = request.GET.get("next")
        self.next = reverse(next) if next else "/"
        return super().setup(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return self.next


class LogoutView(_DjangoLogoutView):
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        next = request.GET.get("next")
        self.next = reverse(next) if next else "/"
        return super().setup(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return self.next

    pass


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        next = request.GET.get("next")
        self.next = reverse(next) if next else "/"
        return super().setup(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return self.next


class PasswordResetView(_DjangoPasswordResetView):
    template_name = "users/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:password_reset_email_sent")
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
