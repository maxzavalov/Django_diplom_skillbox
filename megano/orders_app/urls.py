from django.urls import path
from .views import CartDetailView, OrderApiView, OrderDetailApiView, PaymentApiView

app_name = "orders_app"

urlpatterns = [
    path('orders', OrderApiView.as_view(), name="orders"),
    path('order/<int:pk>', OrderDetailApiView.as_view(), name="order_detail"),
    path('basket', CartDetailView.as_view(), name="basket"),
    path('payment/<int:pk>', PaymentApiView.as_view(), name="payment")
]
