# Generated by Django 5.1.2 on 2024-12-19 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_coupon_restaurant_liked_users_usercoupon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user_coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.usercoupon'),
        ),
    ]
