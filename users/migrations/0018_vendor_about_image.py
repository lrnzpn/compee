# Generated by Django 3.1.1 on 2020-10-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20201004_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='about_image',
            field=models.ImageField(blank=True, null=True, upload_to='store_pics'),
        ),
    ]