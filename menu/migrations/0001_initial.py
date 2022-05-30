# Generated by Django 3.2 on 2022-05-30 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('course', models.IntegerField(choices=[(0, 'Starters'), (1, 'Mains'), (2, 'Desert')])),
                ('price', models.IntegerField()),
            ],
        ),
    ]