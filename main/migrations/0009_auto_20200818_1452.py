# Generated by Django 3.0.7 on 2020-08-18 14:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_siteorder_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteorder',
            name='contact_no',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d+$', 'Only numeric characters are allowed.')]),
        ),
    ]
