import django

from django.db import models

if django.VERSION >= (1, 5):
    from django.contrib.auth.models import AbstractBaseUser, UserManager

    class User(AbstractBaseUser):
        username = models.CharField(max_length=255)
        email = models.EmailField()
        is_active = models.BooleanField()
        is_superuser = models.BooleanField()
        is_staff = models.BooleanField()
        date_joined = models.DateTimeField()

        objects = UserManager()
