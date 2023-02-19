from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="username",
        )

    password = models.CharField(
        max_length=128,
        verbose_name="password",
        )

    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
        verbose_name="email",
        )

    first_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name="first name",
        )

    last_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        verbose_name="last name",
        )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", ]
