from rest_framework_nested.routers import DefaultRouter,NestedDefaultRouter
from django.urls import path,include

from shopcarts.views import CartItemViewset, CartViewset

router = DefaultRouter()
router.register('cart',CartViewset,basename='cart')

cart_nested_router = NestedDefaultRouter(router,'cart',lookup = 'cart')
cart_nested_router.register('item',CartItemViewset,basename='cart-item')

urlpatterns=[
    path('',include(router.urls)),
    path('',include(cart_nested_router.urls)),
]
