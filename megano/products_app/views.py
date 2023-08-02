from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, ReviewSerializers, TagSerializer, CategorySerializer, \
    CatalogProductSerializers, SalesSerializers
from .models import Product, Review, Tag, Category
from .paginations import CustomPagination
from .filters import ProductFilter


class CategoriesListAPIView(APIView):
    """Представление для категорий и подкатегорий"""
    def get(self, request):
        """Get catalog menu"""
        categories = Category.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        print(serialized.data)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ProductAPIView(generics.RetrieveAPIView):
    """Представление для отображения продуктов"""

    queryset = Product.objects.select_related('category', 'specification'). \
        prefetch_related('tags').all()
    serializer_class = ProductSerializer


class CreateReviewAPIView(APIView):
    """Представление для создания отзывов"""
    permission_classes = permissions.IsAuthenticated

    def post(self, request):
        """Создание экземпляра отзыва"""
        serializer = ReviewSerializers(data=request.data)
        if serializer.is_valid():
            review = Review.objects.create(
                author=request.user,
                product=Product.objects.filter(pk=self.kwargs.get("pk")),
                text=request.data.get('text'),
                rate=request.data.get('rate'),
                email=request.user.email
            )
            review.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagAPIView(generics.ListAPIView):
    """Представление для отображения тэгов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CatalogListAPIView(generics.ListAPIView):
    """Представление для отображения каталога продуктов"""
    queryset = Product.objects.all()
    serializer_class = CatalogProductSerializers
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductPopularListAPIView(generics.ListAPIView):
    """Представление для отображения популярных продуктов"""
    queryset = Product.objects.filter(popular=True)
    serializer_class = CatalogProductSerializers


class ProductLimitedListAPIView(generics.ListAPIView):
    """Представление для отображения лимитированных продуктов"""
    queryset = Product.objects.filter(limited=True)
    serializer_class = CatalogProductSerializers


class SaleAPIView(generics.ListAPIView):
    """Представление для отображения продуктов со скидкой"""
    queryset = Product.objects.filter(sale=True)
    serializer_class = SalesSerializers
    pagination_class = CustomPagination
