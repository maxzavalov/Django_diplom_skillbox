from rest_framework import serializers
from .models import Product, Review, Tag, Category


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Product"""

    class Meta:
        model = Product
        fields = ["id", "category", "price", "count", "date", "title", "description", "fullDescription",
                  "freeDelivery", "tags", "reviews", "specifications", "rating"]


class ReviewSerializers(serializers.ModelSerializer):
    """Сериализатор данных для модели Review"""

    class Meta:
        model = Review
        fields = ['text', 'rate', 'product', 'author', 'email', 'date']


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Tag"""

    class Meta:
        model = Tag
        fields = ['name']


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Подкатегория"""

    class Meta:
        model = Category
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Категория"""

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
    """Сериализатор данных модели Product для отображения в каталоге"""

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
        """Метод вычисляет среднюю оценку товара по отзывам"""

        if obj.reviews.count() > 0:
            res = [data.rate for data in obj.reviews.all()]
            return sum(res) / len(res)
        return 0

    def get_reviews(self, obj):
        """Метод вычисляет количество отзывов о товаре"""
        return obj.reviews.count()

    def get_images(self, obj):
        """Метод возвращает ссылки на все изображения для экземпляра продукта"""
        return [
            {
                'src': image.images.url,
                'alt': image.images.name,
            }
            for image in obj.images.all()
        ]


class CatalogSerializers(serializers.ModelSerializer):
    """Сериализатор данных для каталога товаров"""
    items = CatalogProductSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['items']


class SalesSerializers(serializers.ModelSerializer):
    """Сериализатор данных для товаров со скидкой"""
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
        ]

    def get_images(self, obj):
        """Метод возвращает ссылки на все изображения для экземпляра продукта"""
        return [
            {
                'src': image.images.url,
                'alt': image.images.name,
            }
            for image in obj.images.all()
        ]
