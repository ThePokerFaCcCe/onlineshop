from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import OrderViewset,PostTypeViewset


router = DefaultRouter()
router.register('post-type', PostTypeViewset)
router.register('order', OrderViewset,basename='order')


urlpatterns=[
    path('',include(router.urls))    
]
