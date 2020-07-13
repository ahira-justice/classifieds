from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from uuid import uuid4 as uid

from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    id = models.UUIDField(primary_key=True, default=uid, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
