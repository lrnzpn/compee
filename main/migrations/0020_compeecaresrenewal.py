# Generated by Django 3.1.1 on 2020-10-07 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20201007_0702'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompeeCaresRenewal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notes', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Unresolved', 'Unresolved'), ('Resolved', 'Resolved')], default='Unresolved', max_length=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.siteorder')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.orderitem')),
            ],
        ),
    ]
