from django.urls import path,include
from rest_framework_nested.routers import DefaultRouter,NestedDefaultRouter

from .views import OrderItemViewset, OrderViewset,PostTypeViewset


router = DefaultRouter()
router.register('post-type', PostTypeViewset)
router.register('order', OrderViewset,basename='order')

order_nested_router=NestedDefaultRouter(router,'order',lookup='order')
order_nested_router.register('items',OrderItemViewset,basename='order-items')

urlpatterns=[
    path('',include(router.urls)),
    path('',include(order_nested_router.urls)),
]
