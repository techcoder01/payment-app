# Generated by Django 4.0.8 on 2024-05-09 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0009_bankaccount_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_number',
            field=models.CharField(max_length=25),
        ),
    ]