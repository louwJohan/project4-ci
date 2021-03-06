# Generated by Django 3.2 on 2022-06-14 10:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0004_timeslot_number_of_people'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='first_name',
            field=models.CharField(default='First Name', max_length=50),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='last_name',
            field=models.CharField(default='Surname', max_length=50),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='number_of_people',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]
