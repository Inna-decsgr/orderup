# Generated by Django 5.1.2 on 2024-11-02 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_remove_menu_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='available',
        ),
    ]