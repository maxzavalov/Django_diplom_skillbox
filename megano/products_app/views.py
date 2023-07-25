from django.shortcuts import render
from models import Product
from rest_framework.views import APIView
from rest_framework import generics
from serializers import ProductSerializer


class ProductAPIView(generics.RetrieveAPIView):
    """Представление для отображения продуктов"""

    queryset = Product.objects.select_ralated('category', 'specification').prefetch_related('tags').all()
    serializer_class = ProductSerializer







