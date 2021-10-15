from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import PROTECT, SET_NULL
from django.db.models.fields import CharField, DateTimeField, DecimalField, PositiveIntegerField, TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation

from picturic.models import PictureGeneric


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

    if 'social_media'in settings.INSTALLED_APPS:
        from social_media.models import Comment, Like, TaggedItem
        tags = GenericRelation(TaggedItem)
        comments = GenericRelation(Comment)
        likes = GenericRelation(Like)

    pictures = GenericRelation(PictureGeneric)
    category = ForeignKey(to=Category,on_delete=PROTECT, related_name = 'products')
    promotions = ManyToManyField(to=Promotion)

    class Meta:
        ordering=['title']


