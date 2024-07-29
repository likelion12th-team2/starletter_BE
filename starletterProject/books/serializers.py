from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class BookSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.nickname')
    cover = serializers.ImageField(use_url=True, required=False, allow_empty_file=True)
    last_updated = serializers.DateTimeField(required=False, format='%Y-%m-%d')

    class Meta:
        model = Book
        fields = ['id', 'title', 'pet', 'author', 'description', 'cover', 'last_updated', 'keyword_tag']

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book


class PageImageSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(use_url=True)

    class Meta:
        model = PageImage
        fields = ['images']


class PageSerializer(serializers.ModelSerializer):
    book = serializers.ReadOnlyField(source = 'book.title')
    author = serializers.ReadOnlyField(source = 'author.username')
    created_at = serializers.DateTimeField(required=False, format='%Y-%m-%d')
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = obj.images.all() 
        return PageImageSerializer(instance=images, many=True, context=self.context).data

    class Meta:
        model = Page
        fields = [ 'id', 'book', 'author', 'body', 'created_at', 'is_public', 'images' ]

    def create(self, validated_data):
        instance = Page.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('images'):
            PageImage.objects.create(page=instance, images=image_data)
        return instance
    

class NoteSerializer(ModelSerializer):
    book = serializers.ReadOnlyField(source = 'book.title')
    author = serializers.ReadOnlyField(source = 'author.nickname')
    class Meta:
        model = Note
        fields = '__all__'


'''
# 공감하기
class BookMindSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    minds = serializers.StringRelatedField(many=True)

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Book
        fields = [ 'id', 'user', 'minds' ]
'''