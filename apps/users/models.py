from django.contrib.auth.models import AbstractUser
# from django.db import models


class BaseUser(AbstractUser):

    def generate_token(self):
        pass
