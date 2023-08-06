from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Модель категории"""

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(max_length=150, null=False, verbose_name="Название")
    image = models.ImageField(upload_to='catalog_images', verbose_name="Изображение")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="Родительская категория")

    def __str__(self):
        return self.title


class Specification(models.Model):
    """Модель спецификации"""

    name = models.CharField(max_length=150, null=False, blank=True, verbose_name="Параметр")
    value = models.CharField(max_length=200, null=False, blank=True, verbose_name="Значение")

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"


class Tag(models.Model):
    """Модель ярлыков(тэгов)"""

    name = models.CharField(max_length=128, null=False, blank=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="product", verbose_name="Категория")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Стоимость")
    count = models.PositiveIntegerField(blank=True, null=True, verbose_name="Количество")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    title = models.CharField(max_length=300, verbose_name="Название")
    description = models.TextField(null=False, blank=True, verbose_name="Описание")
    fullDescription = models.TextField(null=False, blank=True, verbose_name="Полное описание")
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="product", verbose_name="Тэги")
    specification = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name="product", verbose_name="Спецификации")
    rating = models.PositiveIntegerField(blank=True, null=True, verbose_name="Рейтинг")
    popular = models.BooleanField(default=False, verbose_name='Популярный')
    limited = models.BooleanField(default=False, verbose_name='Лимитированный')
    salePrice = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='Цена со скидкой')
    sale = models.BooleanField(default=False, verbose_name='Скидка')
    dateFrom = models.DateTimeField(blank=True, null=True, verbose_name="Дата начала")
    dateTo = models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """ Модель изображений товара"""

    src = models.ImageField(upload_to='product_images', verbose_name='Ссылка')
    alt = models.CharField(max_length=128, default="Image alt string", verbose_name='Описание')
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, verbose_name="Продукт")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товара"


class Review(models.Model):
    """Модель отзывов"""

    RATE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Пользователь")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Продукт"
    )
    text = models.CharField(blank=True, max_length=1000)
    rate = models.IntegerField(choices=RATE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user id: {self.user.pk} about product id: {self.product.pk}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
