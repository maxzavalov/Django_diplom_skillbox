from django import forms
from django.contrib import admin
from .models import Product, ProductImage, Specification, Review


admin.site.register(Specification)


class ImagesProductInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'rate', 'date')
    readonly_fields = ('author',)


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    search_fields = ('title', 'category')
    list_filter = ('popular', 'limited', 'sale')
    list_display = ('title', 'category', 'price', 'sale', 'popular', 'limited', 'freeDelivery', 'date', 'count')
    inlines = [ImagesProductInline]
    list_editable = ('popular', 'limited', 'freeDelivery')
    readonly_fields = ('date',)
    fieldsets = (
        ('Название и количество', {
            'fields': (('title', 'count', 'date'),)
        }),
        ('Описание товара', {
            'fields': (('description', 'fullDescription'),)
        }),
        ('Статус товара', {
            'classes': ('collapse',),
            'fields': (('sale', 'popular', 'limited', 'freeDelivery'),),
        }),
        ('Цена', {
            'fields': (('price', 'salePrice'),),
        }),
        ('Дата и время действия скидки', {
            'classes': ('collapse',),
            'fields': (('dateFrom', 'dateTo', ),),
        }),
        ('Теги и категории', {
            'fields': (('tags', 'category'),)
        }),
        ('Спецификация', {
            'fields': (('specification',),)
        }),
    )