# Generated by Django 3.2 on 2023-09-30 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20230930_0130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]