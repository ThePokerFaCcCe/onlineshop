from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddressViewset, CustomerViewset

router = DefaultRouter()
router.register('users', CustomerViewset)
router.register('address', AddressViewset)
urlpatterns = [
    path('', include(router.urls))
]
