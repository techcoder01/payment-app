# Generated by Django 4.0.8 on 2024-05-07 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
