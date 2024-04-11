from django.urls import path

from .views import (get_all_products, get_user_cart, update_product,
                    add_or_delete_from_cart, get_or_make_order, create_product)


urlpatterns = [
    path('products', get_all_products),
    path('cart/<int:pk>', add_or_delete_from_cart),
    path('cart', get_user_cart),
    path('order', get_or_make_order),
    path('product/<int:pk>', update_product),
    path('product', create_product)
]
