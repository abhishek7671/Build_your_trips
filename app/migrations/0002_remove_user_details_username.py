# Generated by Django 4.1.8 on 2023-06-12 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_details',
            name='username',
        ),
    ]