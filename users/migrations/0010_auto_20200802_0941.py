# Generated by Django 3.0.7 on 2020-08-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200724_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='slug',
            field=models.SlugField(default='name', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyer',
            name='store_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='store_name',
            field=models.CharField(max_length=100),
        ),
    ]