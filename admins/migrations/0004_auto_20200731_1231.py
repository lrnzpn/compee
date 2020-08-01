# Generated by Django 3.0.7 on 2020-07-31 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_auto_20200728_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='admins.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins.Product')),
            ],
            options={
                'unique_together': {('category', 'product')},
            },
        ),
        migrations.DeleteModel(
            name='ProductTerm',
        ),
        migrations.DeleteModel(
            name='Term',
        ),
    ]
