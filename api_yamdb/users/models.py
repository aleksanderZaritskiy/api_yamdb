from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    bio = models.TextField('Биография', blank=True, null=True)
    # В доке указано, что поле необязательно к заполнению,
    # но почему его пользователь вообще может заполнять?
    role = models.TextField('Роль', blank=True, null=True, default='user')

    def __str__(self):
        return self.username
