# Generated by Django 3.0.7 on 2020-09-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_vendorreview_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=8),
        ),
    ]
