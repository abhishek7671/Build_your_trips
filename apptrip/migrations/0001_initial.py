# Generated by Django 4.1.8 on 2023-05-15 04:27

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FutureTrips',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('trip_name', models.CharField(max_length=100)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('days', models.IntegerField()),
                ('email', djongo.models.fields.JSONField(default=None)),
                ('budget', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
                ('location', djongo.models.fields.JSONField(default=None)),
                ('date_info', models.DateTimeField(auto_now_add=True)),
                ('trip_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PastTravelledTrips',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('trip_name', models.CharField(max_length=100)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('days', models.CharField(max_length=140)),
                ('email', djongo.models.fields.JSONField(default=None)),
                ('budget', models.IntegerField()),
                ('address', models.CharField(max_length=45)),
                ('location', djongo.models.fields.JSONField(default=None)),
                ('date_info', models.DateTimeField(auto_now_add=True)),
                ('trip_id', models.CharField(max_length=200)),
            ],
        ),
    ]
