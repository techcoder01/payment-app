# Generated by Django 4.0.8 on 2024-05-09 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0013_userprofile_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]