# Generated by Django 5.1.2 on 2024-11-01 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_menu_image_menu_image_url_menu_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='orders.optiongroup')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='menus', to='orders.optionitem'),
        ),
    ]
