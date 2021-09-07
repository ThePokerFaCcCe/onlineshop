from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'pk',
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_admin'
        ]
        read_only_fields = fields
