from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Count, Avg
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    TagSerializer,
    CategorySerializer,
    CatalogProductSerializer,
    SalesSerializer,
)
from .models import Product, Review, Tag, Category
from .paginations import CustomPagination
from .filters import CatalogFilter


class CategoriesListAPIView(APIView):
    """Представление для категорий и подкатегорий"""

    def get(self, request):
        """Get catalog menu"""
        categories = Category.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CategoryListAPIView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = CatalogProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self, pk: int):
        category = Category.obgects.get(pk=pk)
        queryset = Product.objects.filter(category=category)
        return queryset



class ProductAPIView(APIView):
    """Представление для отображения продуктов"""

    def get(self, request, pk=None):
        product = generics.get_object_or_404(Product, pk=pk)
        serialized = ProductSerializer(product)
        return Response(serialized.data)


class CreateReviewAPIView(generics.CreateAPIView):
    """Представление для создания отзывов"""

    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product = generics.get_object_or_404(Product, pk=self.kwargs.get("pk"))
        serializer.save(user=self.request.user, product=product)


class TagAPIView(generics.ListAPIView):
    """Представление для отображения тэгов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CatalogListAPIView(generics.ListAPIView):
    """Представление для каталога товаров"""

    queryset = Product.objects.all()
    serializer_class = CatalogProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CatalogFilter
    pagination_class = CustomPagination


class ProductPopularListAPIView(generics.ListAPIView):
    """Представление для отображения популярных продуктов"""

    queryset = Product.objects.filter(popular=True)
    serializer_class = CatalogProductSerializer


class ProductLimitedListAPIView(generics.ListAPIView):
    """Представление для отображения лимитированных продуктов"""

    queryset = Product.objects.filter(limited=True)
    serializer_class = CatalogProductSerializer


class SaleAPIView(APIView):
    """Представление для отображения продуктов со скидкой"""

    def get(self, request):
        sales = Product.objects.filter(sale=True)
        serialized = SalesSerializer(sales, many=True)
        return Response({"items": serialized.data})
