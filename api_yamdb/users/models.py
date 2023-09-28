from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.TextField('Роль', blank=True, null=True, default='user')
    email = models.EmailField('Электронная почта', blank=False, unique=True)

    def __str__(self):
        return self.username
