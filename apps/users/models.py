from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def generate_token(self):
        pass
