from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings

from .models import Order, OrderItem, PostType
from products.models import Product

if 'product_social_media' in settings.INSTALLED_APPS:
    from product_social_media.serializers import SocialProductSerializer as ProductSerializer
else :
    from products.serializers import ProductSerializer

User = get_user_model()


class PostTypeSerializer(serializers.ModelSerializer):
    count_uses = serializers.SerializerMethodField()

    class Meta:
        model = PostType
        fields = [
            'pk',
            'title',
            'description',
            'count_uses',
            'price',
        ]

    def get_count_uses(self, obj):
        return obj.orders.count()


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) #, write_only=True

    class Meta:
        model = OrderItem
        fields = [
            'pk',
            'quantity',
            'price',
            'product',
        ]
        extra_kwargs = {
            'price': {'read_only': True},
        }
        
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance=instance.product).data

        return representation

class OrderSerializer(serializers.ModelSerializer):
    post_type = serializers.PrimaryKeyRelatedField(queryset=PostType.objects.all())

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    products = OrderItemSerializer(source='order_items', many=True)

    class Meta:
        model = Order
        fields = [
            'pk',
            'first_name',
            'last_name',
            'phone_number',
            'email',

            'post_type',
            'post_type_price',
            'country',
            'city',
            'street',
            'postal_code',

            'price',
            'buy_token',

            'status',
            'user',

            'products',
        ]
        extra_kwargs = {
            'email': {'required': False},
            'status': {'required': False},
            'price': {'read_only': True},
            'post_type_price': {'read_only': True},
            # '':{'required':False},
        }

    def validate_products(self, items_data):
        errors = []
        for item_data in items_data:
            if item_data.get('quantity') > item_data.get('product').inventory:
                errors.append({"quantity": f"Order quantity is greater than product inventory with pk=\"{item_data.get('product').pk}\"" })
        if errors:
            raise serializers.ValidationError(errors, code='overflow')
        return items_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.OrderStatus(instance.status).label
        representation['post_type'] = PostTypeSerializer(instance=instance.post_type).data
        return representation

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        post_type_price = validated_data.get('post_type').price

        price = post_type_price

        for item_data in order_items_data:
            product = item_data.get('product')
            order_quantity = item_data.get('quantity')

            product.inventory -= order_quantity
            product.save()

            item_data.price = product.price
            price += (product.price * order_quantity)

        order = Order.objects.create(price=price, post_type_price=post_type_price, **validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, price=item_data.price, **item_data)

        return order

    def update(self, order, validated_data):
        order_items_data = validated_data.get('order_items', None)
        price = order.price

        if order_items_data:
            old_products=[]    
            old_items=OrderItem.objects.select_related('product').filter(order=order)
            for item in old_items:
                product = Product.objects.get(pk=item.product.pk)
                product.inventory+=item.quantity
                product.save()
                old_products.append(product)
                item.delete()
                
            
            order_items_data = validated_data.pop('order_items')

            price = validated_data.get('post_type', order.post_type).price

            for item_data in order_items_data:
                product = item_data.get('product')
                try:
                    search_index = old_products.index(product)
                    product = old_products[search_index]
                    old_products.pop(search_index)
                except ValueError:
                    pass

                order_quantity = item_data.get('quantity')

                product.inventory -= order_quantity
                product.save()

                OrderItem.objects.create(order=order, price=product.price, **item_data)

                price += (product.price * order_quantity)

        else:
            post_type = validated_data.get('post_type', order.post_type)
            if post_type != order.post_type:
                price += post_type.price - order.post_type_price
                order.post_type_price = post_type.price

        order.price = price
        order = super().update(order, validated_data)
        return order
