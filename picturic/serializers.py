# 00/06/21

from rest_framework import serializers
from .models import PictureModel
from .serializer_fields import PictureField

class PictureModelSerializer(serializers.ModelSerializer):
    pic = PictureField()
    class Meta:
        model = PictureModel
        fields=[
            'id',
            'pic',
        ]

