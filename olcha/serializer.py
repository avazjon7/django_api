from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from olcha.models import Category, Group, Product, Image, Comment,ProductAttribute, AttributeKey, AttributeValue


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at
        return representation


class CategorySerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    full_image_url = serializers.SerializerMethodField()
    groups_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'full_image_url', 'created_at', 'updated_at', 'groups_count', 'groups']

    def get_groups_count(self, obj):
        return obj.groups.count()

    def get_full_image_url(self, instance):
        if instance.image:
            request = self.context.get('request')
            return request.build_absolute_uri(instance.image.url) if request else None
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    all_images = serializers.SerializerMethodField()
    users_comment = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    count_comments = serializers.SerializerMethodField(method_name='counts')
    users_like = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='group.category.title')

    def get_ratings(self, obj):
        ratings = obj.comments.all().values_list('rating', flat=True).aggregate(avg=Avg('rating'))
        return ratings

    def get_users_like(self, product):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        if user in product.users_like.all():
            return True

        return False

    def counts(self, obj):
        count = obj.comments.count()
        return count

    def get_all_images(self, obj):
        request = self.context.get('request')
        images = [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
        return images

    def get_users_comment(self, obj):
        comments = [comment.user.username for comment in obj.comments.all()]
        return comments

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        context = super(ProductSerializer, self).to_representation(instance)
        context['updated_at'] = datetime.now()
        return context


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'