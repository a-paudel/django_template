from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    Group as _DjangoGroup,
    UserManager as _DjangoUserManager,
)

from core.models import BaseModel

# Create your models here.


class UserManager(_DjangoUserManager):
    def create_user(self, email, password: str | None = None, **extra_fields) -> Any:
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, password: str | None = None, **extra_fields
    ) -> Any:
        if not email:
            raise ValueError("The Email field must be set")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)
    email_validated_on = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    group: models.ForeignKey["Group"]
    objects: "UserManager" = UserManager()


# proxy for group
class Group(_DjangoGroup):
    users: models.QuerySet["User"]

    class Meta:
        proxy = True
