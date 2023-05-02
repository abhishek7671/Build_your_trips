# Generated by Django 4.1.5 on 2023-05-02 02:41

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='USER_details',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.CharField(choices=[('Normal User', 'Normal User')], default='Normal User', editable=False, max_length=20)),
                ('username', models.CharField(max_length=138)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=138)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]