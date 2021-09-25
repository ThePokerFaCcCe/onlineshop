from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserSerializer as DjoserUserSerializer, UserCreatePasswordRetypeSerializer as DjoserUserCreateSerializer

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
            'is_admin'
        ]
        read_only_fields = fields


class CustomerSerializer(DjoserUserSerializer):
    class Meta:
        model = DjoserUserSerializer.Meta.model
        fields = [
            'id',
            'username',
            # 'email',
            # 'password',
            'first_name',
            'last_name',
            'phone_number',
            'age',
            'profile_image',
            'is_active',
            'is_staff',
            'is_admin',
        ]

        extra_kwargs = {
            # 'password': {'write_only': True},
            # 'email': {'write_only': True},
            'is_active': {'read_only': True},
            'profile_image': {'read_only': True},
            'age': {'required': False},
        }

    def update(self, instance, validated_data):
        # validated_data.pop('password') if validated_data.get('password') else None
        if not self.context['request'].user.is_staff:
            validated_data.pop('username') if validated_data.get('username') else None

        return super().update(instance, validated_data)

class CustomerProfileSerializer(serializers.ModelSerializer):
    profile_image=PictureField(required=True)
    class Meta:
        model=Customer
        fields=[
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
            'profile_image',
        ]
        extra_kwargs = {
            'email': {'write_only': True},
            'profile_image': {'read_only': True},
        }


class CustomerDeleteSerializer(serializers.Serializer):
    pass

class CustomerToAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields=[
            'id',
            'is_staff',
            'is_admin',
        ]
        extra_kwargs={
            'is_staff':{'source':'staff','required':True},
            'is_admin':{'source':'admin','required':True},
        }

class AddressSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)
    class Meta:
        model=Address
        fields=[
            'id',
            'country',
            'city',
            'street',
            'postal_code',
            'user',
        ]
        extra_kwargs={
            'user':{'source':'customer','read_only':True},
        }
