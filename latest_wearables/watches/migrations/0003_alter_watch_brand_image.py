# Generated by Django 5.0.1 on 2024-02-26 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watches', '0002_rename_sellig_price_watch_selling_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='brand_image',
            field=models.ImageField(upload_to='media/watch_images'),
        ),
    ]