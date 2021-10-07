from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from picturic.serializer_fields import MultiplePictureField
from products.schemas import CATEGORY_RESPONSE_RETRIEVE, CATEGORY_RESPONSE_LIST, PRODUCT_RESPONSE_LIST, PRODUCT_RESPONSE_RETRIEVE, PROMOTION_REQUEST, PROMOTION_RESPONSE_RETRIEVE, PROMOTION_RESPONSE_LIST
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

    def _get_pics(self, instance) -> QuerySet:
        pics_queryset = PictureGeneric.objects.filter(
            content_type=ContentType.objects.get_for_model(instance.__class__),
            object_id=instance.pk
        )

        return pics_queryset

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
        print('update')
        if pictures:
            old_pictures = self._get_pics(product)
            # old_pictures.delete() if old_pictures else None
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
        representation['pictures'] = PictureGenericSerializer(self._get_pics(instance), many=True, context=self.context).data

        return representation
