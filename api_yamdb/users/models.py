from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from reviews.validators import validate_name
from reviews.constants import LENGTH_ROLE, LENGTH_USER_NAME, LENGTH_EMAIL


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(unique=True, max_length=LENGTH_EMAIL)
    username = models.CharField(
        max_length=LENGTH_USER_NAME,
        unique=True,
        validators=(validate_name, UnicodeUsernameValidator()),
    )
    role = models.CharField(
        max_length=LENGTH_ROLE, choices=ROLES, default=USER
    )
    bio = models.TextField(
        blank=True,
    )
    first_name = models.CharField(max_length=LENGTH_USER_NAME, blank=True)
    last_name = models.CharField(
        max_length=LENGTH_USER_NAME,
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ['-id']
