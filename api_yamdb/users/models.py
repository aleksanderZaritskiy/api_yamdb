from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class MyUser(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+$')]),
    )
    role = models.CharField(max_length=50, choices=ROLES, default=USER)
    bio = models.TextField(
        blank=True,
    )

    confirmation_code = models.CharField(
        max_length=40,
        blank=True,
        null=True,
    )

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['-id']
