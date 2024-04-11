from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Product, Cart, Order
from .serializers import ProductSerializer, CartSerializer, OrderSerializer
from .permissions import IsClient


@api_view(['GET'])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(
        {
            'data': serializer.data
        }
    )


@api_view(['POST', 'DELETE'])
@permission_classes([IsClient])
def add_or_delete_from_cart(request, pk):
    if request.method == 'DELETE':
        try:
            cart = Cart.objects.get(pk=pk)
        except:
            return Response(
                {
                    'error': {
                        'code': 404,
                        'message': 'item not found'
                    }
                }
            )
        cart.delete()
        return Response(
            {
                'message': 'item removed from cart'
            }
        )
    elif request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(
                {
                    'error': {
                        'code': 404,
                        'message': 'item not found'
                    }
                }
            )
        Cart.objects.create(user=request.user, product=product)
        return Response(
            {
                'message': 'item added to cart'
            }
        )


@api_view(["GET"])
@permission_classes([IsClient])
def get_user_cart(request):
    carts = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(carts, many=True)
    carts = []
    for cart in serializer.data:
        new_cart = {
            'id': cart['id'],
            'product_id': cart['product']['id'],
            'name': cart['product']['name'],
            'description': cart['product']['id'],
            'price': cart['product']['price'],
        }
        carts.append(new_cart)
    return Response(
        {
            'data': carts
        }
    )


@api_view(["GET", "POST"])
@permission_classes([IsClient])
def get_or_make_order(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(
            {
                'data': serializer.data
            }
        )
    elif request.method == 'POST':
        carts = Cart.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user, order_price=0)
        order_price = 0
        for cart in carts:
            order.product.add(cart.product)
            order_price += cart.product.price
            cart.delete()
        order.order_price = order_price
        order.save()
        serializer = OrderSerializer(order)
        return Response(
            {
                'data': serializer.data
            }
        )


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'data': serializer.data
            }
        )
    else:
        return Response(
            {
                'errors': serializer.errors
            }
        )


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response(
            {
                'code': 422,
                'errors': 'Not found'
            }
        )
    if request.method == 'DELETE':
        product.delete()
        return Response(
            {
                'message': 'Product deleted'
            }
        )
    elif request.method == 'PATCH':
        serializer = ProductSerializer(instance=product,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data
                }
            )
        else:
            return Response(
                {
                    'errors': serializer.errors
                }
            )
