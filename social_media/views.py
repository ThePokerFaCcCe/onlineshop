from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from user_perms.permissions import IsAdminOrReadOnly, IsOwnerOfItem
from .models import Tag, Comment
from .serializers import TagSerializer, CommentSerializer


@permission_classes([IsAdminOrReadOnly])
class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@permission_classes([IsOwnerOfItem | IsAdminOrReadOnly])
class CommentViewset(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.prefetch_related('reply').all()
    serializer_class = CommentSerializer

    # Trying to make drf spectacular understands that in update, serializer won't get reply_to field!
    # def get_serializer_class(self):
    #     serializer = self.serializer_class
        
    #     if self.request.method in ['PUT', 'PATCH']:
    #         setattr(serializer.Meta, 'read_only_fields', ('reply_to',))
        
    #     return serializer

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
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def hidden_comments(self,req,*args,**kwargs):
        """Last deleted comments by users"""
        hidden_comments=self.get_queryset().filter(hidden=True).order_by('-created_at')
        serializer = self.get_serializer_class()(hidden_comments,read_only=True,context={'no-reply':True},many=True)

        return Response(serializer.data)
