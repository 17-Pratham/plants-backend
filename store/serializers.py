from rest_framework import serializers
from .models import (
    Category, Product, Blog,
    PlantSpecification, PotSpecification, CareProductSpecification, ProductFAQ
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# 🔥 LIST
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'tag',
            'price',
            'old_price',
            'discount_percentage',
            'has_discount',  
            'image',
            'rating',
            'show_in_search'
        ]


# 🔥 SPEC SERIALIZERS
class PlantSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSpecification
        fields = '__all__'


class PotSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotSpecification
        fields = '__all__'


class CareSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareProductSpecification
        fields = '__all__'

class ProductFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFAQ
        fields = ['id', 'question', 'answer', 'order']

# 🔥 DETAIL
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    faqs = ProductFAQSerializer(many=True, read_only=True)
    plant_spec = PlantSpecSerializer(read_only=True)
    pot_spec = PotSpecSerializer(read_only=True)
    care_spec = CareSpecSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'tags',
            'short_description',
            'content',
            'image',
            'featured',
            'meta_title',
            'meta_description',
            'created_at',
        ]
