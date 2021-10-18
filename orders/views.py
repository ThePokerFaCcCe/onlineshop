from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from utils.core import all_methods
from user_perms.permissions import IsOwnerOfItem, IsAdminOrReadOnly
from .models import Order, OrderItem, PostType
from .serializers import OrderItemUpdateSerializer, OrderSerializer, OrderItemSerializer, OrderUpdateSerializer, PostTypeSerializer


@permission_classes([IsAdminOrReadOnly])
class PostTypeViewset(viewsets.ModelViewSet):
    queryset = PostType.objects.prefetch_related('orders').all()
    serializer_class = PostTypeSerializer


class OrderViewset(viewsets.ModelViewSet):
    lookup_field = 'id'
    http_method_names = all_methods('put')

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = Order.objects

        if self.request.user.is_staff:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(user=self.request.user)

        if self.request.method == 'DELETE':
            return queryset
        if self.request.method == 'PATCH':
            return queryset.prefetch_related('order_items__product')
        return queryset.select_related('user')\
            .prefetch_related('order_items__product__pictures', 'post_type__orders')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewset(viewsets.ModelViewSet):
    lookup_field = 'product_id'
    lookup_url_kwarg = 'product_id'
    http_method_names = all_methods('put')

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        queryset = OrderItem.objects.filter(order_id=order_id)

        if self.request.method == 'DELETE':
            return queryset
        if self.request.method == 'PATCH':
            return queryset.select_related('product')

        return queryset.prefetch_related('product__pictures')

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OrderItemUpdateSerializer
        return OrderItemSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS', 'HEAD']:
            return [permissions.IsAuthenticated()]

        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(order_id=self.kwargs.get('order_id'))
