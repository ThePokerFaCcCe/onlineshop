from django.urls import path,include
from rest_framework.routers import DefaultRouter,Route,DynamicRoute

from .views import CartViewset



# class NoPutRouter(DefaultRouter):
#     """
#     Router class that disables the PUT method.
#     """
#     def get_method_map(self, viewset, method_map):

#         bound_methods = super().get_method_map(viewset, method_map)

#         if 'put' in bound_methods.keys():
#             del bound_methods['put']

#         return bound_methods

class CustomCartRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]






router = CustomCartRouter()
# router = DefaultRouter()
router.register('cart', CartViewset)

urlpatterns = [
    path('',include(router.urls))
]
