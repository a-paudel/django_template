from django.contrib.auth.forms import (
    UserCreationForm as _DjangoUserCreationForm,
    AuthenticationForm as _DjangoAuthenticationForm,
    PasswordResetForm as _DjangoPasswordResetForm,
    SetPasswordForm as _DjangoSetPasswordForm,
)
from core.forms import BaseForm
from users.models import User


class RegisterForm(BaseForm, _DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(BaseForm, _DjangoAuthenticationForm):
    pass


class PasswordResetForm(BaseForm, _DjangoPasswordResetForm):
    pass


class PasswordSetForm(BaseForm, _DjangoSetPasswordForm):
    pass
