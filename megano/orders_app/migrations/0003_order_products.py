# Generated by Django 4.2.3 on 2023-08-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "products_app",
            "0010_remove_review_author_remove_review_email_review_user_and_more",
        ),
        ("orders_app", "0002_orderproduct"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                related_name="products",
                to="products_app.product",
                verbose_name="Продукты",
            ),
        ),
    ]