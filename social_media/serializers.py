from rest_framework import serializers
from .models import Tag,TaggedItem

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
