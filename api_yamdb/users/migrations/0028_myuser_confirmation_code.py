# Generated by Django 3.2 on 2023-10-03 07:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0027_alter_myuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='confirmation_code',
            field=models.CharField(
                blank=True,
                max_length=40,
                null=True,
                verbose_name='Проверочный код',
            ),
        ),
    ]