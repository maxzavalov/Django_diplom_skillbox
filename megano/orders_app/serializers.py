from rest_framework import serializers
from .models import Order
from products_app.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели заказа"""

    fullName = serializers.ReadOnlyField(source="user.profile.fullname")
    email = serializers.ReadOnlyField(source="user.profile.email")
    phone = serializers.ReadOnlyField(source="user.profile.phone")
    products = ProductSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]
