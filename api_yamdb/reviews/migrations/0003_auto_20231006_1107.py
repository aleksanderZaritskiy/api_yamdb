# Generated by Django 3.2 on 2023-10-06 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={
                'default_related_name': 'comments',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.AlterModelOptions(
            name='review',
            options={
                'default_related_name': 'review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(
                help_text='Укажите название',
                max_length=256,
                verbose_name='Название',
            ),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(
                help_text='Укажите слаг. Поле должно быть уникальным',
                unique=True,
                verbose_name='Слаг',
            ),
        ),
        migrations.AlterField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='comments',
            name='review',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='reviews.review',
            ),
        ),
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(
                help_text='Введите текст', verbose_name='Текст'
            ),
        ),
        migrations.AlterField(
            model_name='comments',
            name='title',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='reviews.title',
            ),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(
                help_text='Укажите название',
                max_length=256,
                verbose_name='Название',
            ),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(
                help_text='Укажите слаг. Поле должно быть уникальным',
                unique=True,
                verbose_name='Слаг',
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='review',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(
                help_text='Оцените произведение от 1 до 10',
                verbose_name='Оценка',
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(
                help_text='Введите текст', verbose_name='Текст'
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='review',
                to='reviews.title',
            ),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(
                blank=True,
                help_text='Опишите произведение',
                verbose_name='Описание',
            ),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(
                help_text='Укажите название произведения',
                max_length=256,
                verbose_name='Название произведения',
            ),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(
                help_text='Укажите дату выхода произведения',
                validators=[reviews.validators.validate_year],
                verbose_name='Дата выхода произведения',
            ),
        ),
    ]
