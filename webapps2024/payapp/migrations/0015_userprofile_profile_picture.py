# Generated by Django 4.0.8 on 2024-05-09 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0014_remove_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
