from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField()
    location = models.CharField(max_length=200)
