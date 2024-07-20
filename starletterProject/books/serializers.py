from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class BookSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.nickname')

    class Meta:
        model = Book
        fields = ['id', 'title', 'pet', 'author', 'description', 'cover', 'last_updated', 'keyword_tag']

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book


class PageImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PageImage
        fields = ['image']


class PageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        image = obj.image.all() 
        return PageImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Page
        fields = [ 'id', 'book', 'author', 'body', 'created_at', 'is_public' ]

    def create(self, validated_data):
        instance = Page.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PageImage.objects.create(post=instance, image=image_data)
        return instance
    

class NoteSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.username')
    class Meta:
        models = Note
        fields = [ 'id', 'book', 'author', 'body' ]


# 공감하기
class BookMindSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    minds = serializers.StringRelatedField(many=True)

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Book
        fields = [ 'id', 'user', 'minds' ]