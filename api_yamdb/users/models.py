from django.contrib.auth.models import AbstractUser
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
        null=True,
        unique=True
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['-id']
