# Generated by Django 3.2 on 2022-06-14 11:07

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20220614_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default=0, max_length=128, region=None, unique=True),
        ),
    ]
