from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Tag, TaggedItem, Like, Comment
from products.models import Product


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'label'
        ]


class TaggedItemSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = TaggedItem
        fields = [
            'id',
            'label'
        ]

    def get_label(self, obj):
        return obj.tag.label


class LikeSerializer(serializers.Serializer):
    likes = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'likes',
            'liked_by_user',
        ]

    def get_likes(self, *args, **kwargs) -> int:
        likes_count = Like.objects.filter(
            content_type=self.context.get('content_type'),
            object_id=self.context.get('product').pk,
        ).count()

        return likes_count

    def get_liked_by_user(self, *args, **kwargs) -> bool:
        return self.context.get('liked_by_user')

# class RecursiveField(serializers.Serializer):
#     def to_representation(self,value)->int:
#         serializer = self.parent.parent.__class__(value,context=self.context)
#         return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'reply_to',
            'text',
            'hidden',
            'user',
            'replies',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'hidden': {'read_only': True},
            # 'reply_to': {'read_only': True},
        }

    def get_replies(self, obj) -> list[int]:
        if self.context.get('no-reply'):
            return ['...']
        return self.__class__(obj.reply, many=True).data

    def create(self, validated_data):
        user = self.context['request'].user
        return super().create({**validated_data, "user": user})

    def update(self, instance, validated_data):
        """Change text of comment"""
        instance.text = validated_data.get('text', instance.text)

        # reply_to = validated_data.get('reply_to', instance.reply_to)
        # if instance != reply_to:
        #     instance.reply_to = reply_to

        instance.save()
        return instance
