# Generated by Django 3.2 on 2023-10-02 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0006_rename_reviews_review'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                fields=('author', 'title'), name='unique review'
            ),
        ),
    ]