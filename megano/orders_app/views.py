from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Order, OrderProduct
from .serializers import OrderSerializer
from products_app.models import Product
from .cart import Cart


class OrderApiView(APIView):
    """Представление для получения заказов текущего пользователя и создания новых"""

    def get(self, request: Request):
        order_data = Order.objects.filter(user_id=request.user.pk)
        serialized = OrderSerializer(order_data, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request: Request):
        products_in_order = [(obj["id"], obj["count"], obj["price"]) for obj in request.data]
        print(request.data)
        products = Product.objects.filter(id__in=[obj[0] for obj in products_in_order])
        order = Order.objects.create(
            user=request.user,
            totalCost=sum(i[1] * float(i[2]) for i in products_in_order),
        )
        data = {
            "orderId": order.pk,
        }

        order.products.set(products)
        order.save()
        for product in request.data:
            OrderProduct.objects.create(
                order_id=order.pk,
                product_id=product["id"],
                count=product["count"]
            )
        return Response(data, status=status.HTTP_200_OK)


class OrderDetailApiView(APIView):
    """Представление для получения деталей заказа и заполнения данных"""

    def get(self, request: Request, pk: int) -> Response:
        data = Order.objects.get(pk=pk)
        serialized = OrderSerializer(data)
        cart = Cart(request).cart
        data = serialized.data

        try:
            products_in_order = data['products']
            query = OrderProduct.objects.filter(order_id=pk)
            prods = {obj.product.pk: obj.count for obj in query}
            for prod in products_in_order:
                prod['count'] = prods[prod['id']]
        except Exception:
            products_in_order = data['products']
            for prod in products_in_order:
                prod['count'] = cart[str(prod['id'])]['count']

        return Response(data)

    def post(self, request: Request, pk: int) -> Response:
        order = generics.get_object_or_404(Order, pk=pk)
        data = request.data
        print(data)
        order.fullName = data['fullName']
        order.phone = data['phone']
        order.email = data['email']
        order.deliveryType = data['deliveryType']
        order.city = data['city']
        order.address = data['address']
        order.paymentType = data['paymentType']
        order.status = 'Ожидает оплаты'
        if data['deliveryType'] == 'express':
            order.totalCost += 50
        else:
            if order.totalCost < 200:
                order.totalCost += 20

        order.save()

        return Response(request.data, status=status.HTTP_200_OK)


class CartDetailView(APIView):
    """APIView для корзины, реализация методов get, post и delete"""

    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            cart_items.append(
                {
                    "id": product.id,
                    "category": product.category.id,
                    "price": float(item["price"]),
                    "count": item["quantity"],
                    "date": product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)"),
                    "title": product.title,
                    "description": product.description,
                    "freeDelivery": product.freeDelivery,
                    "images": [
                        {"src": image.src.url, "alt": image.alt}
                        for image in product.images.all()
                    ],
                    "tags": [
                        {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                    ],
                    "reviews": product.reviews.count(),
                    "rating": product.average_rating(),
                }
            )
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)


class PaymentApiView(APIView):
    """Представление для заполнения данных на оплату"""

    def post(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        order.status = 'Оплачен'
        order.save()
        cart = request.session.get('cart', [])
        cart.clear()
        request.session['cart'] = cart
        request.session.save()
        return Response(request.data, status=status.HTTP_200_OK)
