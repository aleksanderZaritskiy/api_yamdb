# Generated by Django 3.2 on 2023-09-29 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20230929_0320'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='myuser',
            name='username_is_not_me',
        ),
    ]
