from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Cart, CartItem
from products.models import Product

if 'product_social_media' in settings.INSTALLED_APPS:
    from product_social_media.serializers import SocialProductSerializer as ProductSerializer
else :
    from products.serializers import ProductSerializer

User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all().only('pk'), write_only=True)

    class Meta:
        model = CartItem
        fields = [
            # 'pk',
            'cart',
            'quantity',
            'product',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance=instance.product,context=self.context).data

        return representation

    def validate(self, data):
        quantity=data.get('quantity')
        if quantity > data.get('product').inventory:            
            # raise serializers.ValidationError({"product": data.get('product').pk, "error": "Cart item quantity is greater than product inventory"},code='overflow')
            raise serializers.ValidationError({"quantity": f"Cart item quantity is greater than product inventory with pk=\"{data.get('product').pk}\"" },code='overflow')
        return data


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    products = CartItemSerializer(source='cart_items', many=True, read_only=True)

    class Meta:
        model = Cart

        fields = [
            'pk',
            'user',
            'products',
        ]
