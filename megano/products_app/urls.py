from django.urls import path
from .views import (
    ProductAPIView,
    TagAPIView,
    CreateReviewAPIView,
    CategoriesListAPIView,
    ProductPopularListAPIView,
    ProductLimitedListAPIView,
    CatalogListAPIView,
    CategoryListAPIView,
    SaleAPIView,
)

app_name = "products_app"

urlpatterns = [
    path("product/<int:pk>/", ProductAPIView.as_view(), name="product"),
    path("product/<int:pk>/reviews/", CreateReviewAPIView.as_view(), name="review"),
    path("tags/", TagAPIView.as_view(), name="tags"),
    path("categories/", CategoriesListAPIView.as_view(), name="categories"),
    path("catalog/", CatalogListAPIView.as_view(), name="catalog"),
    path("catalog/<int:pk>/", CategoryListAPIView.as_view(), name="category"),
    path(
        "products/popular/", ProductPopularListAPIView.as_view(), name="products_popular"
    ),
    path(
        "products/limited/", ProductLimitedListAPIView.as_view(), name="products_limited"
    ),
    path("sales/", SaleAPIView.as_view(), name="products_sales"),
    path("banners/", ProductLimitedListAPIView.as_view(), name="banners"),
]
