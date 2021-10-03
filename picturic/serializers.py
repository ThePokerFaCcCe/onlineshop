# 00/06/21

from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import PictureGeneric
from .serializer_fields import PictureField

class PictureGenericSerializer(serializers.ModelSerializer):
    file = PictureField()
    class Meta:
        model = PictureGeneric
        fields=[
            'id',
            'file',
        ]

    def create(self, validated_data):
        obj = self.context['object']
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return super().create({"object_id":obj.pk,"content_type":content_type,**validated_data})

