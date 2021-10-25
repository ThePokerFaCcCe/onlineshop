from typing import Iterable
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from product_social_media.schemas import SOCIAL_PRODUCT_RESULT_LIST, SOCIAL_PRODUCT_RESULT_RETRIEVE
from products.models import Product
from products.serializers import ProductSerializer
from social_media.models import Tag, TaggedItem
from social_media.serializers import CommentSerializer, TaggedItemSerializer
from customers.serializers import CustomerReadOnlySerializer
from utils import content_types


class CustomCommentSerializer(CommentSerializer):
    user = CustomerReadOnlySerializer(read_only=True)


@extend_schema_serializer(examples=[SOCIAL_PRODUCT_RESULT_RETRIEVE, SOCIAL_PRODUCT_RESULT_LIST])
class SocialProductSerializer(ProductSerializer):
    tags = serializers.ListField(allow_empty=True, write_only=True, required=False, child=serializers.IntegerField(min_value=1))
    likes = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:  # Reason that i didn't used meta inheritance: https://github.com/encode/django-rest-framework/issues/1926#issuecomment-71819507
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
            'tags',
            'likes',
            'liked_by_user',
            # 'comments',
            'comments_count',
        ]

        extra_kwargs = {
            'description': {'required': False},
            'tags': {'required': False}
        }

    def get_comments_count(self, product) -> int:
        return product.comments.count()

    def get_likes(self, product, *args, **kwargs) -> int:
        return product.likes.count()

    def get_liked_by_user(self, product, *args, **kwargs) -> bool:
        user = self.context['request'].user

        if user and user.is_authenticated:
            return product.likes.filter(user=user).count() == 1

        return False

    def validate_tags(self, tags_pk):
        queryset = Tag.objects.all()
        errors = []
        for pk in tags_pk:
            if not queryset.filter(pk=pk):
                errors.append({'tag': f"Invalid pk \"{pk}\" - object does not exist."})

        if errors:
            raise serializers.ValidationError(errors, code='invalid pk')
        return tags_pk

    def _create_tags(self, tags_pk: Iterable, product_id: int):
        return \
            TaggedItem.objects.bulk_create(
                [
                    TaggedItem(tag_id=tag_pk, content_type=content_types.PRODUCT, object_id=product_id)
                    for tag_pk in tags_pk
                ]
            )

    def create(self, validated_data):
        tags_pk = validated_data.pop('tags', [])
        product = super().create(validated_data)
        self._create_tags(tags_pk, product.pk)
        return product

    def update(self, product, validated_data):
        tags_pk = validated_data.pop('tags', [])
        if tags_pk:
            TaggedItem.objects.filter(content_type=content_types.PRODUCT, object_id=product.pk).delete()
            self._create_tags(tags_pk, product.pk)

        return super().update(product, validated_data)

    def to_representation(self, product):
        representation = super().to_representation(product)
        representation['tags'] = TaggedItemSerializer(product.tags, many=True).data

        return representation
