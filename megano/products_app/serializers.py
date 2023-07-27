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


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }
