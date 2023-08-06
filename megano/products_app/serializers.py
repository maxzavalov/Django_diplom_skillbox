from rest_framework import serializers
from .models import Product, Review, Tag, Category, Specification, ProductImage


class ImagesProductSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели изображений продукта"""
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Отзыв(Review)"""
    author = serializers.ReadOnlyField(source='user.profile.fullname')
    email = serializers.ReadOnlyField(source='user.profile.email')

    class Meta:
        model = Review
        fields = (
            'author', 'email', 'text', 'rate', 'date'
        )


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериализации данных для модели Specification"""

    class Meta:
        model = Specification
        fields = ['name', 'value']


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Tag"""

    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Product"""

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription',
            'freeDelivery', 'images', 'tags', 'specification', 'rating', 'reviews'
        ]

    images = ImagesProductSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specification = SpecificationSerializer()
    tags = TagSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj) -> float | int:
        """
        Добавляем поле rating и считаем по обратной связи общее
        количество отзывов, если есть то считаем средний рейтинг продукта
        """
        if obj.reviews.count() > 0:
            res = [o.rate for o in obj.reviews.all()]
            res = sum(res) / len(res)
            return res
        return 0


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Категория"""

    image = serializers.SerializerMethodField()

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

    subcategories = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_subcategories(self, obj):
        return SubCategorySerializer(obj.subcategories.all(), many=True).data

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }


class CatalogProductSerializer(serializers.ModelSerializer):
    """Сериализатор данных модели Product для отображения в каталоге"""

    images = ImagesProductSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "category", "price", "count", "date", "title", "description", "freeDelivery", "images", "tags",
            "reviews", "rating"
        ]

    def get_reviews(self, obj):
        return Review.objects.filter(product=obj).count()


class SalesSerializer(serializers.ModelSerializer):
    """Сериализатор данных для товаров со скидкой"""
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
        ]

    def get_images(self, obj):
        return [{'src': img.images.src, 'alt': img.images.alt} for img in obj.images.all()]
