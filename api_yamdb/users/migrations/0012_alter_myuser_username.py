# Generated by Django 3.2 on 2023-09-29 02:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0011_alter_myuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
    ]
