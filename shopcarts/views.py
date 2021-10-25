from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from shopcarts.models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


class CartViewset(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('cart_items__product__pictures').all()
    serializer_class = CartSerializer

    lookup_field = 'id'

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Cart.objects.all()
        return self.queryset


class CartItemViewset(CreateModelMixin, RetrieveModelMixin,
                      DestroyModelMixin, GenericViewSet):

    serializer_class = CartItemSerializer

    lookup_field = 'product_id'
    lookup_url_kwarg = 'product_id'

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return CartItem.objects.all()
        return CartItem.objects.prefetch_related('product__pictures')\
            .filter(cart_id=self.kwargs.get("cart_id"))

    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs.get("cart_id"),
            'queryset': self.get_queryset(),
            **super().get_serializer_context(),
        }
