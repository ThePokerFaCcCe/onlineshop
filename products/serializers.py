from rest_framework import serializers
from .models import Product, Category, Promotion


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


class CategorySerializer(serializers.ModelSerializer):
    featured_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),required=False,allow_null=True)

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
    

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        if instance.featured_product:
            representation['featured_product'] = FeaturedProductSerializer(instance=instance.featured_product).data

        return representation



class ProductSerializer(serializers.ModelSerializer):
    promotions = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all(), many=True,required=False,allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'inventory',
            'price',
            'category',
            'promotions',
        ]

        extra_kwargs = {
            'description': {'required': False}
        }
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['promotions']=PromotionSerializer(instance=instance.promotions, many=True).data
        representation['category']=ProductCategorySerializer(instance=instance.category).data
        
        return representation

# class CategoryProductsSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True,read_only=True)

#     class Meta:
#         model = Category
#         fields = [
#             'id',
#             'title',
#             'description',
#             'products',
#         ]

#         extra_kwargs = {
#             'description': {"required": False},
#         }
