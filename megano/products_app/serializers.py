from rest_framework import serializers
from models import Product, Review, Tag, Specification, ProductImage


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title", "description", "fullDescription",
                  "freeDelivery", "tags",  "reviews", "specifications", "rating"]


