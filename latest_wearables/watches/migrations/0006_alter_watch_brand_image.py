# Generated by Django 5.0.1 on 2024-03-03 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watches', '0005_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='brand_image',
            field=models.ImageField(upload_to='watch_images'),
        ),
    ]
