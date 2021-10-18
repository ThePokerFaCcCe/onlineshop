from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


from .models import Order, OrderItem, PostType
from shopcarts.models import Cart
from products.models import Product
from products.serializers import ReadOnlyProductSerializer

User = get_user_model()


class PostTypeSerializer(serializers.ModelSerializer):
    count_uses = serializers.SerializerMethodField()

    class Meta:
        model = PostType
        fields = [
            'id',
            'title',
            'description',
            'count_uses',
            'price',
        ]

    def get_count_uses(self, obj):
        return obj.orders.count()


class PostTypeReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = [
            'id',
            'title',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # , write_only=True
    total_price = SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'quantity',
            'price',
            'total_price',
            'product',
        ]
        extra_kwargs = {
            'price': {'read_only': True},
        }

    def validate(self, data):
        quantity = data.get("quantity")
        product = data.get("product")
        if quantity > product.inventory:
            raise serializers.ValidationError({
                "quantity":
                f"Order quantity is greater than product inventory with pk \"{product.pk}\""
            })

        return data

    def get_total_price(self, item: OrderItem) -> int:
        return item.price*item.quantity

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ReadOnlyProductSerializer(instance=instance.product, context=self.context).data

        return representation

    def create(self, validated_data):
        product: Product = validated_data.get("product")

        order_item: OrderItem = OrderItem.objects.create(
            **validated_data, price=product.price
        )

        return order_item


class OrderItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'quantity',
        ]

    def validate(self, data):
        quantity = data.get("quantity")
        product = self.instance.product
        if quantity > product.inventory:
            raise serializers.ValidationError({
                "quantity":
                f"Order quantity is greater than product inventory with pk \"{product.pk}\""
            })

        return data


class OrderSerializer(serializers.ModelSerializer):
    post_type = serializers.PrimaryKeyRelatedField(queryset=PostType.objects.all())

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    shopcart = serializers.UUIDField(write_only=True)
    products = OrderItemSerializer(source='order_items', many=True, read_only=True)
    total_price = SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
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

            'total_price',
            'buy_token',

            'status',
            'user',
            'shopcart',
            'products',
        ]
        extra_kwargs = {
            'email': {'required': False},
            'status': {'read_only': True},
            'post_type_price': {'read_only': True},
        }

    def validate_shopcart(self, shopcart_id):
        shopcart = Cart.objects.prefetch_related('cart_items__product').filter(pk=shopcart_id)
        if not shopcart.exists():
            raise serializers.ValidationError({
                "shopcart": f"Invalid pk \"{shopcart_id}\" - object does not exist."
            })

        shopcart = shopcart.get()

        cart_item_errors = []
        for item in shopcart.cart_items.all():
            if item.quantity > item.product.inventory:
                cart_item_errors.append({
                    "quantity":
                    f"Order quantity is greater than product inventory with pk \"{item.product.pk}\""
                })
        if cart_item_errors:
            raise serializers.ValidationError(cart_item_errors, code='overflow')

        return shopcart

    def get_total_price(self, order: Order):
        return sum([
            item.price * item.quantity
            for item in order.order_items.all()
        ])

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.OrderStatus(instance.status).label
        representation['post_type'] = PostTypeReadOnlySerializer(instance=instance.post_type).data

        return representation

    def create(self, validated_data):
        with transaction.atomic():
            shopcart = validated_data.pop('shopcart')
            post_type_price = validated_data.get('post_type').price

            order = Order.objects.create(post_type_price=post_type_price, **validated_data)

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order, product=item.product,
                    price=item.product.price, quantity=item.quantity
                )
                for item in shopcart.cart_items.all()
            ])

            shopcart.delete()

            return order


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
        ]

    def update(self, order: Order, validated_data):
        status = validated_data.get("status")

        if status == Order.OrderStatus.COMPLETE:
            products = []
            
            for item in order.order_items.all():
                product = item.product
                product.inventory -= item.quantity

                products.append(product)
            print(products)
            Product.objects.bulk_update(products, fields=['inventory'])

        order.status = status
        order.save()

        return order
