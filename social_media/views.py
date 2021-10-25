from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from social_media.schemas import COMMENT_RESPONSE_PAGINATED

from user_perms.permissions import IsAdminOrReadOnly, IsOwnerOfItem
from utils.core import all_methods
from utils.paginations import DefaultLimitOffsetPagination
from .models import Tag, Comment
from .serializers import CommentUpdateSerializer, TagSerializer, CommentSerializer


@permission_classes([IsAdminOrReadOnly])
class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@permission_classes([IsOwnerOfItem | IsAdminOrReadOnly])
class CommentViewset(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.prefetch_related('reply', 'user').all()
    http_method_names = all_methods('put')

    def get_queryset(self):
        if self.request.method == 'DELETE':
            return Comment.objects.all()
        return self.queryset

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return CommentUpdateSerializer
        return CommentSerializer

    def destroy(self, req, *args, **kwargs):
        """if an admin deletes a comment, comment will delete. else, comment will hide"""
        if req.user.is_staff:
            return super().destroy(req, *args, **kwargs)
        else:
            comment = self.get_object()
            if not comment.hidden:
                comment.hidden = True
                # Do I really need to make replies hidden!?
                # for reply in comment.reply.all():
                #     reply.hidden = True
                #     reply.save()
                comment.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=all_methods('get', only_these=True), permission_classes=[permissions.IsAdminUser])
    def hidden_comments(self, req, *args, **kwargs):
        """Last deleted comments by users"""
        hidden_comments = self.get_queryset().filter(hidden=True).order_by('-created_at')
        serializer = self.get_serializer_class()(hidden_comments, read_only=True, context={'no-reply': True}, many=True)

        return Response(serializer.data)


@extend_schema(examples=[COMMENT_RESPONSE_PAGINATED])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ListCreateCommentsViewset(ListModelMixin, CreateModelMixin, GenericViewSet):
    # You should set `content_type`
    # and `object_id_lookup_url`
    # in your subclasses
    content_type: ContentType = None
    object_id_lookup_url: str = None

    serializer_class = CommentSerializer
    pagination_class = DefaultLimitOffsetPagination

    def _get_oid(self):
        return self.kwargs.get(self.object_id_lookup_url)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            content_type=self.content_type,
            object_id=self._get_oid(),
        )
        if self.request.method == 'DELETE':
            return queryset
        return queryset.get_cached_trees()

    def get_serializer_context(self):
        return {
            **super().get_serializer_context(),
            'object_id': self._get_oid(),
            'content_type': self.content_type,
        }

    def perform_create(self, serializer):
        serializer.save(
            content_type=self.content_type,
            object_id=self._get_oid()
        )
