# Generated by Django 3.0.7 on 2020-07-28 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_auto_20200726_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productterm',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.Product'),
        ),
    ]