from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    class Meta:
        abstract = True

    email = models.EmailField('email address', blank=False, null=False, unique=True)
    is_confirmed = models.BooleanField(default=False)
