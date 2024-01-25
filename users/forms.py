from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from core.forms import BaseForm
from users.models import User


class UserLoginForm(BaseForm, AuthenticationForm):
    class Meta:
        model = User


class UserRegisterForm(BaseForm, UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
