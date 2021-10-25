from rest_framework import permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from social_media.views import ListCreateCommentsViewset
from utils.core import all_methods

from .serializers import SocialProductSerializer
from products.views import ProductViewset
from utils.permissions import IsAdminOrReadOnly
from social_media.models import Like
from social_media.serializers import LikeSerializer
from utils import content_types


@permission_classes([IsAdminOrReadOnly])
class SocialProductViewset(ProductViewset):
    queryset = ProductViewset.queryset.prefetch_related('tags__tag', 'comments', 'likes').all()
    serializer_class = SocialProductSerializer

    @action(detail=True, methods=all_methods('post', 'get', only_these=True), permission_classes=[permissions.IsAuthenticatedOrReadOnly], serializer_class=LikeSerializer)
    def like(self, request, id):
        product = self.get_object()
        liked_by_user = False

        if request.method == 'POST':
            user_like, created = Like.objects.get_or_create(
                content_type=content_types.PRODUCT,
                object_id=product.id,
                user=request.user
            )

            if created:
                liked_by_user = True
            else:
                user_like.delete()

        serializer = self.get_serializer_class()(data=request.data, context={"product": product, 'content_type': content_types.PRODUCT, 'liked_by_user': liked_by_user})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class ProductListCreateCommentsViewset(ListCreateCommentsViewset):
    content_type = content_types.PRODUCT
    object_id_lookup_url = 'product_id'
