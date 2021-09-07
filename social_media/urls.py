from django.urls import path, include
from rest_framework import routers
from .views import TagViewset,CommentViewset

router = routers.DefaultRouter()
router.register('tag', TagViewset)
router.register('comment', CommentViewset)

urlpatterns = [
    path('', include(router.urls))
]
