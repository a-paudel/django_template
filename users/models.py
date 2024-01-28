from django.contrib.auth.models import AbstractUser, UserManager, Group as _Group

from core.models import BaseModel
# Create your models here.


class Group(_Group):
    class Meta:
        proxy = True


class User(BaseModel, AbstractUser):
    objects: UserManager["User"]
