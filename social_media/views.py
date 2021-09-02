from rest_framework import viewsets,permissions
from rest_framework.decorators import permission_classes
from user_perms.permissions import IsAdminOrReadOnly
from .models import Tag
from .serializers import TagSerializer

@permission_classes([IsAdminOrReadOnly])
class TagViewset(viewsets.ModelViewSet):
    queryset=Tag.objects.all()
    serializer_class=TagSerializer
