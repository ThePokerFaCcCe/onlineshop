from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from user_perms.permissions import IsAdmin, IsOwnerOfItem, IsSuperUser
from rest_framework import generics, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Address, Customer
from .serializers import AddressSerializer, CustomerToAdminSerializer, CustomerProfileSerializer


@permission_classes([IsAdminUser | IsAuthenticated])
class CustomerViewset(viewsets.ViewSet, generics.GenericAPIView):
    queryset = Customer.objects.defer('password').all()

    @action(detail=True, methods=['patch', 'put'], permission_classes=[IsSuperUser], serializer_class=CustomerToAdminSerializer)
    def admin_perms(self, req, pk):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=req.data, partial=(req.method == 'PATCH'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsOwnerOfItem|IsAdmin],
            serializer_class=CustomerProfileSerializer, parser_classes=(MultiPartParser,))
    def profile_image(self, req, pk):
        user = self.get_object()
        if req.method == 'POST':
            serializer = self.get_serializer_class()(user, data=req.data, context={'request': req})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer_class()(user, context={'request': req})

        return Response(data=serializer.data)


@permission_classes([IsAuthenticated, IsAdmin | IsOwnerOfItem])
class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_staff or self.request.user.is_admin):
            queryset = queryset.filter(customer=self.request.user)
        return queryset
