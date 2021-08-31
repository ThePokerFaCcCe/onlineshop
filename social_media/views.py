from rest_framework import viewsets,permissions
from rest_framework.decorators import permission_classes
from .models import Tag
from .serializers import TagSerializer

@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class TagViewset(viewsets.ModelViewSet):
    queryset=Tag.objects.all()
    serializer_class=TagSerializer
