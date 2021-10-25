from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from picturic.serializer_fields import MultiplePictureField
from products.schemas import CATEGORY_RESPONSE_RETRIEVE, CATEGORY_RESPONSE_LIST, PRODUCT_RESPONSE_LIST, PRODUCT_RESPONSE_RETRIEVE, PROMOTION_REQUEST, PROMOTION_RESPONSE_RETRIEVE, PROMOTION_RESPONSE_LIST, SIMPLE_PRODUCT_RETRIEVE
from .models import Product, Category, Promotion
from picturic.serializers import PictureGenericSerializer
from picturic.models import PictureGeneric


@extend_schema_serializer(examples=[PROMOTION_RESPONSE_RETRIEVE, PROMOTION_RESPONSE_LIST, PROMOTION_REQUEST])
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            'id',
            'description',
            'discount',
        ]

        extra_kwargs = {
            'description': {'required': False}
        }


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'description',
        ]


class FeaturedProductSerializer(serializers.ModelSerializer):
    promotions = PromotionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'inventory',
            'price',
            'promotions',
        ]


@extend_schema_serializer(examples=[CATEGORY_RESPONSE_RETRIEVE, CATEGORY_RESPONSE_LIST])
class CategorySerializer(serializers.ModelSerializer):
    featured_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, allow_null=True)

    class Meta:

        model = Category
        fields = [
            'id',
            'title',
            'description',
            'featured_product',
        ]

        extra_kwargs = {
            'description': {"required": False}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.featured_product:
            representation['featured_product'] = FeaturedProductSerializer(instance=instance.featured_product).data

        return representation


@extend_schema_serializer(examples=[PRODUCT_RESPONSE_RETRIEVE, PRODUCT_RESPONSE_LIST])
class ProductSerializer(serializers.ModelSerializer):
    promotions = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all(), many=True, required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    pictures = MultiplePictureField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'pictures',
            'inventory',
            'price',
            'category',
            'promotions',
        ]

        extra_kwargs = {
            'description': {'required': False},
        }

    def validate_pictures(self, *args):
        pics = self.context['request'].FILES.getlist("pictures")

        serializer = PictureGenericSerializer(data=[{'file': pic} for pic in pics], many=True)
        serializer.is_valid(raise_exception=True)

        return serializer

    def create(self, validated_data):
        pictures: PictureGenericSerializer = validated_data.pop('pictures')

        product = super().create(validated_data)

        pictures.context.update({'object': product})
        pictures.save()

        return product

    def update(self, instance, validated_data):
        pictures: PictureGenericSerializer = validated_data.pop('pictures', None)
        product = super().update(instance, validated_data)
        if pictures:
            old_pictures = instance.pictures.all()
            if old_pictures:
                for pic in old_pictures:
                    pic.file.delete()
                    pic.delete()
            pictures.context.update({'object': product})
            pictures.save()
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['promotions'] = PromotionSerializer(instance=instance.promotions, many=True).data
        representation['category'] = ProductCategorySerializer(instance=instance.category).data

        representation['pictures'] = PictureGenericSerializer(instance.pictures, many=True, context=self.context).data
        return representation


@extend_schema_serializer(examples=[SIMPLE_PRODUCT_RETRIEVE])
class ReadOnlyProductSerializer(serializers.ModelSerializer):
    pictures = PictureGenericSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'pictures',
        ]
        read_only_fields = fields
