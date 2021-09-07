from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from .serializers import SocialProductSerializer, CustomCommentSerializer
from products.views import ProductViewset
from products.models import Product
from user_perms.permissions import IsAdminOrReadOnly
from social_media.models import Like, Comment
from social_media.serializers import LikeSerializer


@permission_classes([IsAdminOrReadOnly])
class SocialProductViewset(ProductViewset):
    serializer_class = SocialProductSerializer

    @action(detail=True, methods=['post', 'get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly], serializer_class=LikeSerializer)
    def like(self, request, pk):
        product = self.get_object()
        content_type = ContentType.objects.get_for_model(Product)
        liked_by_user = False

        if request.method == 'POST':
            user_like, created = Like.objects.get_or_create(
                content_type=content_type,
                object_id=product.pk,
                user=request.user
            )

            if created:
                liked_by_user = True
            else:
                user_like.delete()

        serializer = self.get_serializer_class()(data=request.data, context={"product": product, 'content_type': content_type, 'liked_by_user': liked_by_user})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='comments/(?P<page>\d+)', serializer_class=CustomCommentSerializer)
    def comments_list(self, request, pk, page):
        product = self.get_object()
        content_type = ContentType.objects.get_for_model(Product)

        from_index = settings.COMMENT_PER_PAGE * (int(page)-1)
        to_index = from_index + settings.COMMENT_PER_PAGE

        comments = Comment.objects.prefetch_related('reply').filter(
            content_type=content_type,
            object_id=product.pk,
            reply_to=None
        )[from_index:to_index]

        if not comments:
            raise Http404()

        serializer = self.get_serializer_class()(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path="comments", serializer_class=CustomCommentSerializer, permission_classes=[permissions.IsAuthenticated])
    def comments_create(self, request, pk):
        product = self.get_object()
        content_type = ContentType.objects.get_for_model(Product)

        serializer = self.get_serializer_class()(data=request.data, context={'no-reply': True, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(object_id=product.pk, content_type=content_type)
        return Response(serializer.data)
