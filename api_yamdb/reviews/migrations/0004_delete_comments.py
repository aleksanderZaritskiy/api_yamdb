# Generated by Django 3.2 on 2023-09-26 06:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0003_alter_csvimport_csv_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
