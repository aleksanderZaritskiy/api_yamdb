# Generated by Django 3.2 on 2023-10-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0023_alter_myuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
    ]
