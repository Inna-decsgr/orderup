# Generated by Django 5.1.2 on 2024-10-22 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='business_registration_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]
