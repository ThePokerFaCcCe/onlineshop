from rest_framework.decorators import action, permission_classes


from products.views import ProductViewset
from .serializers import SocialProductSerializer
from user_perms.permissions import IsAdminOrReadOnly

@permission_classes([IsAdminOrReadOnly])
class SocialProductViewset(ProductViewset):
    serializer_class  = SocialProductSerializer
