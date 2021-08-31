from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import OrderViewset,PostTypeViewset


router = DefaultRouter()
router.register('posttype', PostTypeViewset)
router.register('order', OrderViewset)


urlpatterns=[
    path('',include(router.urls))    
]
