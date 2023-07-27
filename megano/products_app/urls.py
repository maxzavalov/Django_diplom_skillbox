from django.urls import path
from .views import ProductAPIView, TagAPIView, CreateReviewAPIView, CategoriesListAPIView


app_name = "products_app"

urlpatterns = [
    path('product/<int:pk>', ProductAPIView.as_view(), name="product"),
    path('product/<int:pk>/review', CreateReviewAPIView.as_view(), name="review"),
    path('tags', TagAPIView.as_view(), name="tags"),
    path('categories', CategoriesListAPIView.as_view(), name="categories"),
]