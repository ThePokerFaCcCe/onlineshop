from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.core.validators import MinLengthValidator
from django.db.models.fields import CharField, DateTimeField, PositiveIntegerField, EmailField, TextField
from django.db.models import TextChoices
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from django_countries.fields import CountryField

from customers.models import Address
from products.models import Product

User = settings.AUTH_USER_MODEL


class PostType(Model):
    title = CharField(max_length=120)
    description = TextField(max_length=255, null=True, blank=True)
    price = PositiveIntegerField()


class Order(Model):

    class OrderStatus(TextChoices):
        WAITING='W','Waiting'
        PACKING='P', 'Packing'
        SENDING='S','Sending'
        FAIL='F', 'Failed'
        COMPLETE='C', 'Completed'

    status = CharField(max_length=1, choices=OrderStatus.choices, default=OrderStatus.WAITING)

    first_name = CharField(max_length=120)
    last_name = CharField(max_length=120)
    email = EmailField(verbose_name='Email address', max_length=100, null=True, blank=True)
    phone_number = CharField(max_length=32, validators=[MinLengthValidator(6)])

    country = CountryField(default="IR")
    city = CharField(max_length=60)
    street = CharField(max_length=255)
    postal_code = CharField(max_length=50)

    post_type_price=PositiveIntegerField()
    # price = PositiveIntegerField()
    buy_token = CharField(max_length=255)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    post_type = ForeignKey(to=PostType, on_delete=PROTECT, related_name='orders')
    user = ForeignKey(to=User, on_delete=CASCADE, related_name='orders')


class OrderItem(Model):
    quantity = PositiveIntegerField()
    price = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    product = ForeignKey(to=Product, on_delete=PROTECT, related_name="order_items")
    order = ForeignKey(to=Order, on_delete=CASCADE, related_name="order_items")
