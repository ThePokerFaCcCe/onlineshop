from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField, PositiveIntegerField, UUIDField
from django.db.models.fields.related import ForeignKey
from uuid import uuid4

from products.models import Product


class Cart(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class CartItem(Model):
    quantity = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    product = ForeignKey(to=Product, on_delete=CASCADE, related_name='cart_items')
    cart = ForeignKey(to=Cart, on_delete=CASCADE, related_name='cart_items')
