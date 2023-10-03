# Generated by Django 3.2 on 2023-10-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0007_review_unique review'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique review',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                fields=('author', 'title'), name='unique_review'
            ),
        ),
    ]
