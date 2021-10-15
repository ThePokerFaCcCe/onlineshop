from rest_framework_nested import routers
from .views import ProductListCreateCommentsViewset, SocialProductViewset
from django.urls import include,path

router=routers.DefaultRouter()
router.register('product',SocialProductViewset,basename='product')

product_comments_router = routers.NestedDefaultRouter(router,'product',lookup='product')
product_comments_router.register('comments',ProductListCreateCommentsViewset,basename='product-comment')

urlpatterns=[
    path('',include(router.urls)),
    path('',include(product_comments_router.urls)),
]
