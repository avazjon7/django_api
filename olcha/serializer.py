from rest_framework import serializers
from olcha.models import Category, Group, Product, ProductAttributeValue, ProductImage, Image, Comment


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(method_name='groups_count')

    def groups_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'groups_count']
        read_only_fields = ['id', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'value', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount', 'quantity', 'slug', 'attributes']
        read_only_fields = ['id', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discount', 'quantity', 'description', 'slug', 'group_id', 'attributes']
        read_only_fields = ['id', 'slug']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'title', 'image', 'slug', 'products']
        read_only_fields = ['id', 'slug']


class CategoriesGroupsProductsSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'slug', 'groups']
        read_only_fields = ['id', 'slug']\

class CommentSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['message', 'file', 'rating', 'user', 'created_at', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()