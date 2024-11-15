# Generated by Django 5.1.2 on 2024-11-14 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_order_payment_details_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', '주문 접수'), ('delivered', '배달 중'), ('canceled', '주문 취소')], max_length=20),
        ),
    ]