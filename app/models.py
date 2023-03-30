from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    mobile = models.CharField(default=None, max_length=15, blank=True, null=True)
