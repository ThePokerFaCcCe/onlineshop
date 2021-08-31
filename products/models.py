from django.db.models.base import Model
from django.db.models.deletion import PROTECT, SET_NULL
from django.db.models.fields import CharField, DateTimeField, DecimalField, PositiveIntegerField, TextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields.related import ForeignKey, ManyToManyField


class Category(Model):
    title = CharField(max_length=55)
    description = TextField(max_length=255,null=True,blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    featured_product = ForeignKey(to='Product',on_delete=SET_NULL,null=True,blank=True, related_name='featured_product')
    
    class Meta:
        ordering=['title']

class Promotion(Model):
    description = TextField(max_length=255,null=True,blank=True)
    discount = DecimalField(max_digits=5,decimal_places=2,validators=[
        MinValueValidator(0),MaxValueValidator(100)
    ])
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']
    


class Product(Model):
    title = CharField(max_length=100)
    description = TextField(max_length=255,null=True,blank=True)
    price = PositiveIntegerField()
    inventory = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    category = ForeignKey(to=Category,on_delete=PROTECT, related_name = 'products')
    promotions = ManyToManyField(to=Promotion)

    class Meta:
        ordering=['title']


