from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer, UserCreatePasswordRetypeSerializer as DjoserUserCreateSerializer
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


class CustomerSerializer(DjoserUserSerializer):
    class Meta:
        model = DjoserUserSerializer.Meta.model
        fields = [
            'pk',
            'username',
            # 'email',
            # 'password',
            'first_name',
            'last_name',
            'phone_number',
            'age',
            'is_active',
            'is_staff',
            'is_admin',
        ]

        extra_kwargs = {
            # 'password': {'write_only': True},
            # 'email': {'write_only': True},
            'is_active': {'read_only': True},
            'age': {'required': False}
        }

    def update(self, instance, validated_data):
        # validated_data.pop('password') if validated_data.get('password') else None
        if not self.context['request'].user.is_staff:
            validated_data.pop('username') if validated_data.get('username') else None

        return super().update(instance, validated_data)


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
            'pk',
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
        fields=[
            'pk',
            'is_staff',
            'is_admin',
        ]
        extra_kwargs={
            'is_staff':{'source':'staff','required':True},
            'is_admin':{'source':'admin','required':True},
        }
