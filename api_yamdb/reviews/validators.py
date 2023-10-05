from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(data):
    """Валидация даты выхода произведения"""

    today = timezone.now().year
    if data > today:
        raise ValidationError('Нельзя добавить произведение ещё не вышедшее')


def validate_name(data):
    """Валидация имени me"""
    if data == 'me':
        raise ValidationError('Нельзя создать пользователя с именем "me"')
