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

    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text=(
            'Укажите свою электронную почту. '
            'На неё вам придёт письмо с кодом подтвержедния'
        ),
        unique=True,
        max_length=LENGTH_EMAIL,
        error_messages={'max_length': "не валидный имейл больше 254 символов"},
    )
    username = models.CharField(
        verbose_name='Псевдоним',
        help_text='Укажите ваш псевдоним',
        max_length=LENGTH_USER_NAME,
        unique=True,
        validators=(validate_name, UnicodeUsernameValidator()),
        error_messages={'max_length': "больше 150 символов"},
    )
    role = models.CharField(
        verbose_name='Роль',
        help_text='Укажите роль пользователя',
        max_length=LENGTH_ROLE,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='биография пользователя',
        help_text='Укажите биография пользователя',
        blank=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Укажите имя',
        max_length=LENGTH_USER_NAME,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Укажите фамилию',
        max_length=LENGTH_USER_NAME,
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ['-id']
