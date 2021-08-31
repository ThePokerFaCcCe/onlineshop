from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey

from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL

class Cart(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    user = ForeignKey(to=User,on_delete=CASCADE,unique=True)


class CartItem(Model):
    quantity = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    product = ForeignKey(to=Product,on_delete=CASCADE,related_name='cart_items')
    cart = ForeignKey(to=Cart,on_delete=CASCADE,related_name='cart_items')
