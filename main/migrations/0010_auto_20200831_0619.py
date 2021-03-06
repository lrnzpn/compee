# Generated by Django 3.0.7 on 2020-08-31 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200818_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('details', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='siteorder',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.PaymentMethod'),
        ),
    ]
