from django.http import JsonResponse, HttpResponse

from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import permission_classes, action, api_view
from rest_framework.response import Response

from .models import Promotion, Product, Category
from .serializers import CategorySerializer, ProductSerializer, PromotionSerializer


@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("featured_product").all()  # prefetch_related('products').
    serializer_class = CategorySerializer

    @action(detail=True,methods=['get'])
    def products(self, req, *args, **kwargs):
        category = self.get_object()
        serializer = ProductSerializer(category.products, many=True)
        return Response(serializer.data)
    
    @action(detail=True,methods=['delete'])
    def clear_featured_product(self,req,*args,**kwargs):
        category = self.get_object()
        category.featured_product = None
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class PromotionViewset(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("promotions").select_related('category').all()
    serializer_class = ProductSerializer


# TEST
@api_view(['POST', 'GET'])
def userinfo(req):
    print(req.user.is_authenticated)
    return HttpResponse(req.user.age)

# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# class CategoryList(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# class PromotionList(generics.ListCreateAPIView):
#     queryset = Promotion.objects.all()
#     serializer_class = PromotionSerializer


# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# class PromotionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Promotion.objects.all()
#     serializer_class = PromotionSerializer


# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# class ProductList(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# @permission_classes([permissions.IsAuthenticatedOrReadOnly])
# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
