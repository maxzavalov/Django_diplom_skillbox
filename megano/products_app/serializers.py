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


class CatalogProductSerializers(serializers.ModelSerializer):
    """Товары со скидкой"""
    tags = TagSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "category", "price", "count", "date", "title", "description", "freeDelivery", "images", "tags",
            "reviews", "rating"
        ]

    def get_rating(self, obj):
        """
        Добавляем поле rating и считаем по обратной связи общее
        количество отзывов, если есть то считаем средний рейтинг продукта
        """
        if obj.reviews.count() > 0:
            res = [data.rate for data in obj.reviews.all()]
            return sum(res) / len(res)
        return 0

    def get_reviews(self, obj):
        """Добавляем поле reviews и считаем по обратной связи общее количество отзывов"""
        return obj.reviews.count()

    def get_images(self, obj):
        """Добавляем поле images и по обератной связи получаем все изображения данного продукта"""
        return [
            {
                'src': image.images.url,
                'alt': image.images.name,
            }
            for image in obj.images.all()
        ]


class CatalogSerializers(serializers.ModelSerializer):
    """Каталог товаров"""
    items = CatalogProductSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['items']


class SalesSerializers(serializers.ModelSerializer):
    """Товары со скидкой"""
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
        ]

    def get_images(self, obj):
        """Добавляем поле images и по обератной связи получаем все изображения данного продукта"""
        return [
            {
                'src': image.images.url,
                'alt': image.images.name,
            }
            for image in obj.images.all()
        ]
