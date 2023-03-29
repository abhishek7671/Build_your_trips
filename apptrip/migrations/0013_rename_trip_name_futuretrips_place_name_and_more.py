# Generated by Django 4.1.4 on 2023-03-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptrip', '0012_alter_futuretrips_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='futuretrips',
            old_name='trip_name',
            new_name='Place_name',
        ),
        migrations.RenameField(
            model_name='pasttravelledtrips',
            old_name='trip_name',
            new_name='Place_name',
        ),
        migrations.RemoveField(
            model_name='futuretrips',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='futuretrips',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='futuretrips',
            name='people',
        ),
        migrations.RemoveField(
            model_name='pasttravelledtrips',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='pasttravelledtrips',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='pasttravelledtrips',
            name='people',
        ),
        migrations.AddField(
            model_name='futuretrips',
            name='End_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='futuretrips',
            name='Start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pasttravelledtrips',
            name='End_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pasttravelledtrips',
            name='Start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='futuretrips',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
