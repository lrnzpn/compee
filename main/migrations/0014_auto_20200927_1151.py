# Generated by Django 3.0.7 on 2020-09-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20200927_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteorder',
            name='ref_id',
            field=models.CharField(blank=True, default='200927115123C0A8E6', max_length=100, unique=True),
        ),
    ]
