from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as _DjangoGroup

from core.models import BaseModel

# Create your models here.


class User(AbstractUser, BaseModel):
    email_validated_on = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    group: models.ForeignKey["Group"]


# proxy for group
class Group(_DjangoGroup):
    users: models.QuerySet["User"]

    class Meta:
        proxy = True
