from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from django.db.models.signals import pre_save
from django.dispatch import receiver


class BaseUser(AbstractUser):
    token = models.CharField(max_length=36, blank=False, unique=True, null=False)

    @receiver(pre_save, sender='users.BaseUser')
    def generate_token(sender, instance, **kwargs):
        instance.token = str(uuid4()).replace('-', '')
