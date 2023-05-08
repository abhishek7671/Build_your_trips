# Generated by Django 4.1.8 on 2023-05-08 07:02

import apptrip.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ftrip', djongo.models.fields.EmbeddedField(model_container=apptrip.models.FutureTrips)),
                ('build', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FutureTrips',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Trip_name', models.CharField(max_length=100)),
                ('Start_date', models.DateField(blank=True, null=True)),
                ('End_date', models.DateField(blank=True, null=True)),
                ('days', models.IntegerField()),
                ('Email', models.EmailField(max_length=70)),
                ('Budget', models.IntegerField()),
                ('address', models.CharField(max_length=50)),
                ('location', djongo.models.fields.JSONField(default=None)),
                ('date_info', models.DateTimeField(auto_now_add=True)),
                ('trip_id', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='PastTravelledTrips',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('Trip_name', models.CharField(max_length=100)),
                ('Start_date', models.DateField(blank=True, null=True)),
                ('End_date', models.DateField(blank=True, null=True)),
                ('days', models.IntegerField()),
                ('Email', models.EmailField(max_length=70)),
                ('Budget', models.IntegerField()),
                ('address', models.CharField(max_length=45)),
                ('location', djongo.models.fields.JSONField(default=None)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreviousTrips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptrip', djongo.models.fields.EmbeddedField(model_container=apptrip.models.PastTravelledTrips)),
                ('headline', models.CharField(max_length=225)),
            ],
        ),
    ]
