from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import RawSQL
from django.http import JsonResponse, HttpResponse

from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import permission_classes, action, api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from picturic.models import PictureGeneric
from utils.core import all_methods
from utils.filters import OrderingFilterWithSchema

from utils.paginations import DefaultLimitOffsetPagination
from products.filters import ProductFilter
from .models import Promotion, Product, Category
from .serializers import CategorySerializer, ProductSerializer, PromotionSerializer
from user_perms.permissions import IsAdminOrReadOnly


@permission_classes([IsAdminOrReadOnly])
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("featured_product").all()  # prefetch_related('products').
    serializer_class = CategorySerializer

    @action(detail=True, methods=all_methods('get', only_these=True))
    def products(self, req, *args, **kwargs):
        category = self.get_object()
        serializer = ProductSerializer(category.products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=all_methods('delete', only_these=True))
    def clear_featured_product(self, req, *args, **kwargs):
        category = self.get_object()
        category.featured_product = None
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAdminOrReadOnly])
class PromotionViewset(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


@permission_classes([IsAdminOrReadOnly])
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("promotions", 'pictures').select_related('category').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilterWithSchema]
    serializer_class = ProductSerializer
    pagination_class = DefaultLimitOffsetPagination
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'title', 'category_id', 'price']

    lookup_field = 'id'

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Product.objects.all()
        return self.queryset
