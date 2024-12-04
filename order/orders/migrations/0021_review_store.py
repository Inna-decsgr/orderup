# Generated by Django 5.1.2 on 2024-12-04 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='orders.restaurant'),
        ),
    ]
