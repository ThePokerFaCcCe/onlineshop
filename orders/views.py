from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from user_perms.permissions import IsOwnerOfItem,IsAdminOrReadOnly
from .models import Order, OrderItem, PostType
from .serializers import OrderSerializer, OrderItemSerializer, PostTypeSerializer


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


@permission_classes([IsOwnerOfItem|permissions.IsAdminUser])
class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'post_type').prefetch_related('order_items').all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=all_methods(only='get'),permission_classes=[permissions.IsAuthenticated])
    def my_orders(self, req):
        orders_queryset = self.get_queryset().filter(user=req.user)
        serializer = self.get_serializer_class()(orders_queryset, many=True, read_only=True)
        return Response(data=serializer.data)
