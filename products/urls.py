from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewset, ProductViewset, PromotionViewset,userinfo
# from .views import CategoryList, CategoryDetail, PromotionDetail, PromotionList, ProductDetail, ProductList

router = routers.DefaultRouter()
router.register('category', CategoryViewset)
router.register('product', ProductViewset)
router.register('promotion', PromotionViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('userinfo', userinfo),
    # path('category/', CategoryList.as_view()),
    # path('category/<int:pk>/', CategoryDetail.as_view()),

    # path('product/', ProductList.as_view()),
    # path('product/<int:pk>/', ProductDetail.as_view()),

    # path('promotion/', PromotionList.as_view()),
    # path('promotion/<int:pk>/', PromotionDetail.as_view()),
]
