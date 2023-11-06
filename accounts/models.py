from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.email} - {self.username}"
