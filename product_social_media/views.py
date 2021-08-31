from rest_framework.decorators import action
from products.views import ProductViewset
from .serializers import SocialProductSerializer

class SocialProductViewset(ProductViewset):
    serializer_class  = SocialProductSerializer
