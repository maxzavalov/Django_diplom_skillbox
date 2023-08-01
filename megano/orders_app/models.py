from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """Модель заказа"""

    DELIVERY_TYPE = [
        ('free', 'Free'),
        ('paid', 'Paid')
    ]
    PAYMENT_TYPE = [
        ('online', 'Online'),
        ('offline', 'Offline')
    ]
    STATUS = [
        ('accepted', 'Accepted'),
        ('processing', 'Processing'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order", verbose_name="Пользователь")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    address = models.CharField(max_length=250, blank=True, verbose_name="Адрес")
    totalCost = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Итоговая цена")
    deliveryType = models.CharField(max_length=15, choices=DELIVERY_TYPE, verbose_name="Тип доставки")
    paymentType = models.CharField(max_length=15, choices=PAYMENT_TYPE, verbose_name="Тип оплаты")
    status = models.CharField(max_length=15, choices=STATUS, verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
