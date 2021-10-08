from django.db.models import fields
from django_filters.rest_framework import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
            'promotions': ['exact'],
            'price': ['gt', 'lt'],
        }
