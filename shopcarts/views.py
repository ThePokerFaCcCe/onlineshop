from django.db.utils import IntegrityError
from django.http import HttpRequest, Http404, QueryDict
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from user_perms.permissions import IsOwnerOfItem



def all_methods(*args):
    methods = viewsets.ModelViewSet.http_method_names
    return [m for m in methods if m not in args] if args else methods


@permission_classes([IsOwnerOfItem, permissions.IsAuthenticated])
class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.prefetch_related("cart_items").all()
    serializer_class = CartSerializer

    def set_kwarg_lookup(self, req):
        """Looks for user's cart and if doesn't exists, creates one and sets the kwarg of pk to cart.pk"""
        cart = self.queryset.filter(user=req.user).first()
        if not cart:
            cart = self.queryset.create(user=req.user)
        cart_id = cart.pk
        kwarg_field = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[kwarg_field] = cart_id
        return cart_id


    def destroy(self, request):
        """Clear items in a cart"""
        self.set_kwarg_lookup(request)
        cart = self.get_object()
        CartItem.objects.filter(cart=cart).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request):
        """List items in a cart"""
        self.set_kwarg_lookup(request)
        return super().retrieve(request)

    @action(detail=True, methods=all_methods('patch', 'post'), url_path='cart_item/(?P<product_id>\d+)')
    def cart_item(self, req, product_id, *args, **kwargs):
        pk = self.set_kwarg_lookup(req)
        res = CartItemViewset.as_view({'put': 'create', 'get': "retrieve", "delete": "destroy"})(req._request, cart=pk, product=product_id)
        return Response(data=res.data or res.status_text, status=res.status_code)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            pass


# @permission_classes([IsOwnerOfItem, permissions.IsAuthenticated])
class CartItemViewset(viewsets.ModelViewSet):
    queryset = CartItem.objects.select_related("cart").all()
    model = CartItem.objects
    serializer_class = CartItemSerializer

    # data_pk_fieldname = 'product_id'

    def create(self, req, *args, **kwargs):
        """Add or update an item in cart"""
        raw_req = HttpRequest()
        raw_req.data = {**kwargs, **req.data}
        raw_req.method = req.method

        kwarg_field = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[kwarg_field] = kwargs['product']  # req.data.get(self.data_pk_fieldname, None)

        try:
            return self.update(raw_req, *args, **kwargs)
        except Http404:
            return super().create(raw_req, *args, **kwargs)

    def destroy(self, req, *args, **kwargs):
        """Remove an item from cart"""
        raw_req = HttpRequest()
        raw_req.data = {**kwargs, **req.data}
        raw_req.method = req.method

        kwarg_field = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[kwarg_field] = kwargs['product']  # req.data.get(self.data_pk_fieldname, None)

        return super().destroy(raw_req, *args, **kwargs)

    def retrieve(self, req, *args, **kwargs):
        """Show info about an item in cart"""
        raw_req = HttpRequest()
        raw_req.data = {**kwargs, **req.data}
        raw_req.method = req.method

        return super().retrieve(raw_req, *args, **kwargs)
