# Generated by Django 3.1.1 on 2020-10-18 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0028_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='')),
            ],
        ),
    ]