from django.contrib.auth.models import AbstractUser, UserManager

from core.models import BaseModel
# Create your models here.


class User(BaseModel, AbstractUser):
    objects: UserManager["User"]
