# from products.urls import router
from rest_framework import routers
from .views import SocialProductViewset
from django.urls import include,path

router=routers.DefaultRouter()
router.register('product',SocialProductViewset)

urlpatterns=[
    path('',include(router.urls))
]
