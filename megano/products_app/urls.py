from django.urls import path
from views import ProductAPIView

urlpatterns = [
    path('product/<int:pk>', ProductAPIView.as_view(), name="product"),
    path('product/<int:pk>', ProductAPIView.as_view(), name="product")
]