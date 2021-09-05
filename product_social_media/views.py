from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from products.views import ProductViewset
from products.models import Product
from .serializers import SocialProductSerializer
from user_perms.permissions import IsAdminOrReadOnly
from social_media.models import Like
from social_media.serializers import LikeSerializer
@permission_classes([IsAdminOrReadOnly])
class SocialProductViewset(ProductViewset):
    serializer_class  = SocialProductSerializer

    @action(detail=True,methods=['post','get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly], serializer_class=LikeSerializer)
    def like(self,req,pk):
        product = self.get_object()
        content_type = ContentType.objects.get_for_model(Product)
        liked_by_user = False

        if req.method == 'POST':
            user_like, created = Like.objects.get_or_create(
                content_type=content_type,
                object_id=product.pk,
                user=req.user
            )

            if created:
                liked_by_user=True
            else:
                user_like.delete()

        serializer = self.get_serializer_class()(data=req.data,context={"product":product,'content_type':content_type,'liked_by_user':liked_by_user})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

        


