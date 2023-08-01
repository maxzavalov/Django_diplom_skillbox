# Generated by Django 4.2.3 on 2023-07-27 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0002_remove_product_reviews_review_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('image', models.ImageField(upload_to='catalog_images', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]