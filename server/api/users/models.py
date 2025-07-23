from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, null=True, max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = CloudinaryField(folder='Dashboard/avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email