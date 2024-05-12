from typing import Any
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView as _DjangoLoginView, LogoutView as _DjangoLogoutView
from django.urls import reverse
from django.views.generic import CreateView

from users.forms import LoginForm, RegisterForm
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
