from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from user_perms.permissions import IsOwnerOfItem, IsAdminOrReadOnly
from .models import Order, OrderItem, PostType
from .serializers import OrderSerializer, OrderItemSerializer, OrderUpdateSerializer, PostTypeSerializer


def all_methods(*args, **kwargs):
    use_only = kwargs.get('only', None)
    if use_only:
        req_methods = ['put', 'post', 'patch', 'delete', 'get']
        req_methods.remove(use_only.lower())
        args = req_methods

    methods = viewsets.ModelViewSet.http_method_names
    return [m for m in methods if m not in args] if args else methods


@permission_classes([IsAdminOrReadOnly])
class PostTypeViewset(viewsets.ModelViewSet):
    queryset = PostType.objects.prefetch_related('orders').all()
    serializer_class = PostTypeSerializer


class OrderViewset(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.request.method=='PATCH':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related(
            'order_items__product__pictures',
            'post_type__orders'
        )

        if self.request.user.is_staff:
            return queryset.all()

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
