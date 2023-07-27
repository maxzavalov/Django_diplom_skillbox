from django.shortcuts import render
from .models import Product, Review, Tag, Category
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import ProductSerializer, ReviewSerializers, TagSerializer, CategorySerializer
from rest_framework import status, permissions
from rest_framework.response import Response


class CategoriesListAPIView(generics.ListAPIView):
    """Представление для категорий и подкатегорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAPIView(generics.RetrieveAPIView):
    """Представление для отображения продуктов"""

    queryset = Product.objects.select_related('category', 'specification').prefetch_related('tags').all()
    serializer_class = ProductSerializer


class CreateReviewAPIView(APIView):
    """Представление для создания отзывов"""
    permission_classes = permissions.IsAuthenticated

    def post(self, request, *args, **kwargs):
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
