# Generated by Django 3.0.7 on 2020-08-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200802_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]