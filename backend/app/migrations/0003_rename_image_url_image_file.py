# Generated by Django 5.0.2 on 2024-03-04 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_url',
            new_name='file',
        ),
    ]