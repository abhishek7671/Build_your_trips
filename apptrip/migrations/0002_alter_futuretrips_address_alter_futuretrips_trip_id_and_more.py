# Generated by Django 4.1.8 on 2023-05-12 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptrip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='futuretrips',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='futuretrips',
            name='trip_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='futuretrips',
            name='user_id',
            field=models.CharField(max_length=200),
        ),
    ]
