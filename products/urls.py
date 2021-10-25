from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewset, ProductViewset, PromotionViewset

router = routers.DefaultRouter()
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('promotion', PromotionViewset, basename='promotion')

urlpatterns = [
    path('', include(router.urls)),
]
