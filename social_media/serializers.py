from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from social_media.schemas import COMMENT_RESPONSE_LIST, COMMENT_RESPONSE_RETRIEVE
from .models import Tag, TaggedItem, Like, Comment


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

    def get_label(self, obj) -> str:
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


@extend_schema_serializer(examples=[COMMENT_RESPONSE_RETRIEVE, COMMENT_RESPONSE_LIST])
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
        }

    def validate_reply_to(self, reply):
        if reply:
            if not (
                reply.content_type == self.context.get("content_type")
                and
                reply.object_id == int(self.context.get("object_id"))
            ):
                raise serializers.ValidationError({
                    "reply_to": f"Invalid pk \"{reply}\" - object does not exist."
                })
        return reply

    def get_replies(self, obj) -> list[int]:
        if self.context.get('no-reply'):
            return ['...']
        return self.__class__(obj.get_children(), many=True, context=self.context).data

    def create(self, validated_data):
        user = self.context['request'].user
        return super().create({**validated_data, "user": user})


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
        ]
