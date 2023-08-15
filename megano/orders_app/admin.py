from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Регистрация модели Заказ в админке"""

    list_display = ["pk", "user", "totalCost", "createdAt", "status"]
    list_display_links = ["pk", "user"]
