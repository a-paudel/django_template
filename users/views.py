from typing import Any
from urllib.parse import quote
from django.http import HttpRequest
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from users.forms import UserLoginForm, UserRegisterForm

# Create your views here.


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True
    redirect_field_name = "next"

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get("next", "/")
        self.next = "/" + self.next[1:]
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["next"] = quote(self.next)
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        return self.next


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get("next", "/")
        self.next = "/" + self.next[1:]
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["next"] = quote(self.next)
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        return self.next


class UserLogoutView(LogoutView):
    next_page = "/"
