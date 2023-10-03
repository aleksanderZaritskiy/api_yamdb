from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название фильма', max_length=256)
    year = models.IntegerField('Дата выхода')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GengeTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title',
    )

    def __str__(self):
        return self.name


class GengeTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'GengeTitle'

    def __str__(self):
        return f'{self.title} : {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_reviews',
    )
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_reviews',
    )
    score = models.IntegerField('Оценка')
    pub_date = models.DateTimeField(
        'Дата публикации оценки',
        auto_now_add=True,
    )

    class Meta:
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:50]


class Comments(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review_comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата публикации оценки',
        auto_now_add=True,
    )

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[:50]


class CsvImport(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
