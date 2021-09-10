from user_perms.permissions import IsSuperUser
from rest_framework import generics, serializers, viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerToAdminSerializer


class CustomerViewset(viewsets.ViewSet, generics.GenericAPIView):
    queryset = Customer.objects.defer('password').all()

    @action(detail=True, methods=['patch', 'put'], permission_classes=[IsSuperUser], serializer_class=CustomerToAdminSerializer)
    def admin_perms(self, req, pk):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=req.data, partial=(req.method=='PATCH'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
