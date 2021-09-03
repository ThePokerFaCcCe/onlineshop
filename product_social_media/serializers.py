from django.db.utils import ProgrammingError
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from social_media.models import Tag, TaggedItem
from social_media.serializers import TagSerializer, TaggedItemSerializer


# try:
#     product_content_type = ContentType.objects.get_for_model(Product)
# except ProgrammingError:
#     print("WARNING: We couldn't get ContentType model in database, if you are trying to migrate, don't care about this message")

class SocialProductSerializer(ProductSerializer):
    tags = serializers.ListField(allow_empty=True,write_only=True ,child=serializers.IntegerField(min_value=1))
    class Meta:  # Reason that i didn't used meta inheritance: https://github.com/encode/django-rest-framework/issues/1926#issuecomment-71819507
        model = Product
        fields = [
            'pk',
            'title',
            'description',
            'inventory',
            'price',
            'category',
            'promotions',
            'tags',
        ]

        extra_kwargs = {
            'description': {'required': False},
            'tags': {'required': False}
        }

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
            content_type=ContentType.objects.get_for_model(Product), # Django will cache this queryset once, so at second call it doesn't send query to db
            object_id=product.pk
        )
        representation['tags']=[]
        if tagged_items_queryset:
            representation['tags'] = TaggedItemSerializer(tagged_items_queryset, many=True).data

        return representation

    def create(self, validated_data):
        tags_pk = validated_data.pop('tags')
        product = super().create(validated_data)
        for tag_pk in tags_pk:
            TaggedItem.objects.create(tag_id=tag_pk, content_type=product_content_type, object_id=product.pk)
        return product

    def update(self, product, validated_data):
        tags_pk = validated_data.get('tags', None)
        if tags_pk:
            validated_data.pop('tags')
            TaggedItem.objects.filter(content_type=product_content_type, object_id=product.pk).delete()
            for tag_pk in tags_pk:
                TaggedItem.objects.create(tag_id=tag_pk, content_type=product_content_type, object_id=product.pk)

        return super().update(product, validated_data)
