from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddressViewset, CustomerViewset


router = DefaultRouter()
router.register('users', CustomerViewset, basename='users')
router.register('address', AddressViewset)

app_name = 'customers'

urlpatterns = [
    path('', include(router.urls))
]
