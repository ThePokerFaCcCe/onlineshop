from django.db.models import query
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from user_perms.permissions import IsAdmin, IsOwnerOfItem, IsSuperUser
from rest_framework import generics, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .models import Address, Customer
from .serializers import AddressSerializer, CustomerToAdminSerializer

@permission_classes([IsAdminUser|IsAuthenticated])
class CustomerViewset(viewsets.ViewSet, generics.GenericAPIView):
    queryset = Customer.objects.defer('password').all()

    @action(detail=True, methods=['patch', 'put'], permission_classes=[IsSuperUser], serializer_class=CustomerToAdminSerializer)
    def admin_perms(self, req, pk):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=req.data, partial=(req.method=='PATCH'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

@permission_classes([IsAuthenticated,IsAdmin|IsOwnerOfItem])
class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(customer=self.request.user)
    
    def get_queryset(self):
        queryset= super().get_queryset()
        if not (self.request.user.is_staff or self.request.user.is_admin):
            queryset=queryset.filter(customer=self.request.user)
        return queryset
        