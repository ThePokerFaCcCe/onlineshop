from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreatePasswordRetypeSerializer as DjoserUserCreateSerializer
)

from picturic.serializer_fields import PictureField
from .models import Address, Customer


class CustomerReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'id',
            'username',
            'is_active',
            'is_staff',
            'is_superuser'
        ]
        read_only_fields = fields


class CustomerSerializer(DjoserUserSerializer):
    profile_image = PictureField(read_only=True)

    class Meta:
        model = DjoserUserSerializer.Meta.model
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'age',
            'profile_image',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

        extra_kwargs = {
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
            'email': {'read_only': True},
            'username': {'read_only': True},
            'age': {'required': False},
        }


class CustomerProfileSerializer(serializers.ModelSerializer):
    profile_image = PictureField(required=True)

    class Meta:
        model = Customer
        fields = [
            'pk',
            'profile_image',
        ]


class CustomerCreateSerializer(DjoserUserCreateSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"},
            write_only=True,
        )

    class Meta:
        model = DjoserUserCreateSerializer.Meta.model
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'age',
        ]
        extra_kwargs = {
            'email': {'write_only': True},
        }


class CustomerDeleteSerializer(serializers.Serializer):
    pass


class CustomerToAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'is_staff',
            'is_superuser',
        ]
        extra_kwargs = {
            'is_staff': {'required': True},
            'is_superuser': {'required': True},
        }


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'country',
            'city',
            'street',
            'postal_code',
            'user',
        ]
        extra_kwargs = {
            'user': {'source': 'customer', 'read_only': True},
        }
