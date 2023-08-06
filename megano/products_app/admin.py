from django.contrib import admin
from .models import Tag, Product, ProductImage, Specification, Review, Category

admin.site.register(Specification)


class ImagesProductInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    """Регистрация модели Ярлык(Тэг) в админке"""

    list_display = ('pk', 'name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели Категория в админке"""

    list_display = ("__str__",)
    fieldsets = (
        ('Категория', {
            'fields': (('title', 'image', 'parent'),)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Регистрация модели Отзыв в админке"""
    list_display = ('text', 'rate', 'date')


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    """Регистрация модели Продукт в админке"""

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
            'fields': (('dateFrom', 'dateTo',),),
        }),
        ('Теги и категории', {
            'fields': (('tags', 'category'),)
        }),
        ('Спецификация', {
            'fields': (('specification',),)
        }),
    )
