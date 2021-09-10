from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewset

router=DefaultRouter()
router.register('users',CustomerViewset)
urlpatterns=[
    path('',include(router.urls))
]
