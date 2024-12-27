# Generated by Django 5.1.2 on 2024-12-27 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_usercoupon_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='usercoupon',
            name='used_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
