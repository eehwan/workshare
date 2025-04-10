from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    profile_image = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username