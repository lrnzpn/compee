# Generated by Django 3.1.1 on 2020-10-09 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0023_auto_20201009_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displaygroup',
            name='enabled',
            field=models.BooleanField(choices=[('False', 'False'), ('True', 'True')], default=False),
        ),
    ]