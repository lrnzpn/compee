# Generated by Django 3.0.7 on 2020-07-23 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_buyer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer',
            old_name='account',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='vendor',
            old_name='account',
            new_name='user',
        ),
    ]
