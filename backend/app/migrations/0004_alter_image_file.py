# Generated by Django 5.0.2 on 2024-03-04 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_image_url_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
