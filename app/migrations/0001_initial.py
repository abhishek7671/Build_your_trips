# Generated by Django 4.1.7 on 2023-04-10 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=70, unique=True)),
                ('password', models.CharField(default=None, max_length=180)),
            ],
        ),
    ]
