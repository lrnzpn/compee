# Generated by Django 3.0.7 on 2020-08-04 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0009_buyerproductcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyerproductcategory',
            old_name='b_product',
            new_name='product',
        ),
        migrations.AlterUniqueTogether(
            name='buyerproductcategory',
            unique_together={('category', 'product')},
        ),
    ]