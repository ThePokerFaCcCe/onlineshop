from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Tag,TaggedItem,Like
from products.models import Product

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=[
            'pk',
            'label'
        ]


class TaggedItemSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    class Meta:
        model=TaggedItem
        fields=[
            'pk',
            'label'
        ]
    def get_label(self,obj):
        return obj.tag.label

class LikeSerializer(serializers.Serializer):
    likes = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    class Meta:
        fields=[
            'likes',
            'liked_by_user',
        ]
    
    def get_likes(self,*args,**kwargs)->int:
        likes_count = Like.objects.filter(
            content_type=self.context.get('content_type'),
            object_id  = self.context.get('product').pk,
        ).count()

        return likes_count

    def get_liked_by_user(self,*args,**kwargs)->bool:
        return self.context.get('liked_by_user')
