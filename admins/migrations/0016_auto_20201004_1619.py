# Generated by Django 3.1.1 on 2020-10-04 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0015_auto_20201004_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicecategory',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.service'),
        ),
        migrations.AlterField(
            model_name='serviceitemcategory',
            name='service_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.serviceitem'),
        ),
    ]