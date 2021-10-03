from django.db.utils import ProgrammingError
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from social_media.models import Tag, TaggedItem, Like, Comment
from social_media.serializers import TagSerializer, TaggedItemSerializer, CommentSerializer
from customers.serializers import CustomerReadOnlySerializer
from typing import List
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
# try:
#     product_content_type = ContentType.objects.get_for_model(Product)
# except ProgrammingError:
#     print("WARNING: We couldn't get ContentType model in database, if you are trying to migrate, don't care about this message")


class CustomCommentSerializer(CommentSerializer):
    user = CustomerReadOnlySerializer(read_only=True)


@extend_schema_serializer(examples=[OpenApiExample(
    name='Example',
    response_only=True,
    value={
        "id": 0,
        "title": "string",
        "description": "string",
        "pictures": [
            {
                'id':0,
                "file":{
                    "image": {
                        "url": "string",
                        "name": "string"
                    },
                    "thumbnail": {
                        "url": "string",
                        "name": "string"
                    }
                }
            }
        ],
        "inventory": 4294967295,
        "price": 4294967295,
        "category": 0,
        "promotions": [
            0
        ],
        "likes": 0,
        "liked_by_user": True,
        "comments_count": 0
    }
)])
class SocialProductSerializer(ProductSerializer):
    tags = serializers.ListField(allow_empty=True, write_only=True,required=False, child=serializers.IntegerField(min_value=1))
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

    # def get_comments(self,product) -> CommentSerializer(many=True):
    #     comments = Comment.objects.prefetch_related('reply').filter(
    #         content_type=ContentType.objects.get_for_model(Product),
    #         object_id=product.pk,
    #         reply_to=None
    #     )[:settings.COMMENT_PER_PAGE]
    #     serializer = CommentSerializer(comments,many=True)
    #     return serializer.data

    def get_comments_count(self, product) -> int:
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(Product),
            object_id=product.pk,
        ).count()

    def get_likes(self, product, *args, **kwargs) -> int:
        likes_count = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Product),
            object_id=product.pk,
        ).count()

        return likes_count

    def get_liked_by_user(self, product, *args, **kwargs) -> bool:
        user = self.context['request'].user
        is_liked = False
        if user and user.is_authenticated:
            user_like = Like.objects.filter(
                content_type=ContentType.objects.get_for_model(Product),
                object_id=product.pk,
                user=user
            )
            if user_like:
                is_liked = True
        return is_liked

    def validate_tags(self, tags_pk):
        queryset = Tag.objects.all()
        errors = []
        for pk in tags_pk:
            if not queryset.filter(pk=pk):
                errors.append({'tag': f"Invalid pk \"{pk}\" - object does not exist."})

        if errors:
            raise serializers.ValidationError(errors, code='invalid pk')
        return tags_pk

    def to_representation(self, product):
        representation = super().to_representation(product)
        tagged_items_queryset = TaggedItem.objects.select_related('tag').filter(
            content_type=ContentType.objects.get_for_model(Product),  # Django will cache this queryset once, so at second call it doesn't send query to db
            object_id=product.pk
        )
        representation['tags'] = []
        if tagged_items_queryset:
            representation['tags'] = TaggedItemSerializer(tagged_items_queryset, many=True).data

        return representation

    def create(self, validated_data):
        tags_pk = validated_data.pop('tags',[])
        product = super().create(validated_data)
        for tag_pk in tags_pk:
            TaggedItem.objects.create(tag_id=tag_pk, content_type=product_content_type, object_id=product.pk)
        return product

    def update(self, product, validated_data):
        tags_pk = validated_data.pop('tags',[])
        if tags_pk:
            TaggedItem.objects.filter(content_type=product_content_type, object_id=product.pk).delete()
            for tag_pk in tags_pk:
                TaggedItem.objects.create(tag_id=tag_pk, content_type=product_content_type, object_id=product.pk)

        return super().update(product, validated_data)
