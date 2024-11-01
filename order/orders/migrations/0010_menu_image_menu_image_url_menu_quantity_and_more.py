# Generated by Django 5.1.2 on 2024-11-01 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_restaurant_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='image',
            field=models.ImageField(null=True, upload_to='menus/'),
        ),
        migrations.AddField(
            model_name='menu',
            name='image_url',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='menu',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='menus',
            field=models.ManyToManyField(blank=True, related_name='restaurants', to='orders.menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='orders.restaurant'),
        ),
    ]
