# Generated by Django 5.1.2 on 2024-12-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_review_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='review',
            field=models.BooleanField(default=False),
        ),
    ]
