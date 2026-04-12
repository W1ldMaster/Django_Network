from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    avatar = models.ImageField(verbose_name='Аватар', upload_to='users/', blank=False)
