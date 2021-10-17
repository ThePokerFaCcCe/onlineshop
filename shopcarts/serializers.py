from django.conf import settings
from django.http.response import Http404
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Cart, CartItem
from products.models import Product

from products.serializers import ReadOnlyProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    total_price = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'quantity',
            'total_price',
            'product',
        ]

    def validate(self, data):
        cart_id = self.context.get("cart_id")
        if not Cart.objects.filter(pk=cart_id).exists():
            # raise serializers.ValidationError({"cart_id": f"Invalid pk \"{cart_id}\" - object does not exist."})
            raise Http404

        quantity = data.get('quantity')
        if quantity > data.get('product').inventory:
            raise serializers.ValidationError({"quantity": f"Cart item quantity is greater than product inventory with pk=\"{data.get('product').pk}\""}, code='overflow')

        data['cart_id'] = cart_id
        return data

    def get_total_price(self, cart_item: CartItem) -> int:
        return cart_item.product.price * cart_item.quantity

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ReadOnlyProductSerializer(instance=instance.product, context=self.context).data

        return representation

    def create(self, validated_data):
        item = self.context['queryset'].filter(
            product_id=validated_data.get("product"),
        )
        if item.exists():
            item=item.get()
            item.quantity = validated_data.get("quantity", item.quantity)
            item.save()
            return item

        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    products = CartItemSerializer(source='cart_items', many=True, read_only=True)
    total_price = SerializerMethodField()

    class Meta:
        model = Cart

        fields = [
            'id',
            'total_price',
            'products',
        ]

    def get_total_price(self, cart: Cart) -> int:
        return sum([
            item.product.price*item.quantity
            for item in cart.cart_items.all()
        ])
