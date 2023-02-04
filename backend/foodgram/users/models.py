from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 'admin'
    USER = 'user'

    role_choices = (
        (USER, 'user'),
        (ADMIN, 'admin')
    )

    username = models.CharField(max_length=150, unique=True,
                                verbose_name='username')
    password = models.CharField(max_length=128, blank=True,
                                verbose_name='password')
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='email')
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='first name')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='last name')
    bio = models.TextField(blank=True, verbose_name='biography')
    role = models.CharField(
        choices=role_choices,
        default=USER,
        max_length=9,
        verbose_name='role'
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser
