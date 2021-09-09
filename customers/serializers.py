from rest_framework import serializers
from .models import Customer


class CustomerReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'pk',
            'username',
            'is_active',
            'is_staff',
            'is_admin'
        ]
        read_only_fields = fields
