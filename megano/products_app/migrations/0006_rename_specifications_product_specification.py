# Generated by Django 4.2.3 on 2023-07-30 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0005_product_datefrom_product_dateto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='specifications',
            new_name='specification',
        ),
    ]
