from rest_framework import serializers
from .models import Product, Review, Tag, Specification, ProductImage, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title", "description", "fullDescription",
                  "freeDelivery", "tags", "reviews", "specifications", "rating"]


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'rate', 'product', 'author', 'email', 'date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'image']
