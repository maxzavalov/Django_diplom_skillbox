from rest_framework import serializers
from .models import Order, OrderProduct
from products_app.models import Review
from products_app.serializers import ProductSerializer


# class OrderProductSerializer(serializers.ModelSerializer):
#     """Сериализатор данных продуктов для заказа"""
#
#     id = serializers.ReadOnlyField(source="product.id")
#     category = serializers.ReadOnlyField(source="product.category.id")
#     price = serializers.ReadOnlyField(source='product.price')
#     date = serializers.ReadOnlyField(source='product.date')
#     title = serializers.ReadOnlyField(source='product.title')
#     description = serializers.ReadOnlyField(source='product.description')
#     freeDelivery = serializers.ReadOnlyField(source='product.freeDelivery')
#     images = ImagesProductSerializer(source='product.images', many=True)
#     tags = TagSerializer(source='product.tags', many=True)
#     reviews = serializers.SerializerMethodField()
#     rating = serializers.ReadOnlyField(source='product.rating')
#     count = serializers.ReadOnlyField()
#
#     class Meta:
#         model = OrderProduct
#         fields = [
#             "id", "category", "price", "count", "date", "title", "description",
#             "freeDelivery", "images", "tags", "reviews", "rating"
#         ]
#
#     def get_reviews(self, obj):
#         return Review.objects.filter(product=obj.product).count()


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели заказа"""

    fullName = serializers.ReadOnlyField(source='user.profile.fullname')
    email = serializers.ReadOnlyField(source='user.profile.email')
    phone = serializers.ReadOnlyField(source='user.profile.phone')
    products = ProductSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = [
            "id", "createdAt", "fullName", "email", "phone", "deliveryType", "paymentType",
            "totalCost", "status", "city", "address", "products"
        ]
