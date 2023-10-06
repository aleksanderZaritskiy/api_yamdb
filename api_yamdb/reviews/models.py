from django.db import models
from django.contrib.auth import get_user_model

from reviews.constants import MAX_SYMBOL, LENGTH_SLUG, LENGTH_NAME
from .validators import validate_year

User = get_user_model()


class TypeOfArt(models.Model):
    """Абстрактный класс для моделей category и genre"""

    name = models.CharField(
        verbose_name='Название',
        help_text='Укажите название',
        max_length=LENGTH_NAME,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Укажите слаг. Поле должно быть уникальным',
        max_length=LENGTH_SLUG,
        unique=True,
    )

    class Meta:
        abstract = True


class Category(TypeOfArt):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(TypeOfArt):
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        help_text='Укажите название произведения',
        max_length=LENGTH_NAME,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода произведения',
        help_text='Укажите дату выхода произведения',
        validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Опишите произведение',
        blank=True,
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title',
    )

    def __str__(self):
        return self.name


class UsersFeedBack(models.Model):
    """Абстрактный класс для моделей review и comments"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст',
    )
    pub_date = models.DateTimeField(
        'Дата публикации оценки',
        auto_now_add=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text[:MAX_SYMBOL]


class Review(UsersFeedBack):
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        help_text='Оцените произведение от 1 до 10',
    )

    class Meta:
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]
        default_related_name = 'review'


class Comments(UsersFeedBack):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'Comments'
        default_related_name = 'comments'


class CsvImport(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
