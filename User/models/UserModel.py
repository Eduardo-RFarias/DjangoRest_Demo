from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.SlugField(primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    objects = UserManager()
