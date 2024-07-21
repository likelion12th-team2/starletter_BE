from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import User
from .models import UserInfo, PetInfo


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 아이디 중복확인
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호 형식 체크 
    )
    name = serializers.CharField(max_length=30, required=True)
    nickname = serializers.CharField(
        max_length=100,
        required=True,
        validators=[UniqueValidator(queryset=UserInfo.objects.all())], # 닉네임 중복확인
    )
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user_info = UserInfo.objects.create(
            user=user,
            name=validated_data['name'],
            nickname=validated_data['nickname']
        )
        return user, user_info
    

class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    nickname = serializers.CharField(
        max_length=100,
        required=True,
        validators=[UniqueValidator(queryset=UserInfo.objects.all())]
    )
    class Meta:
        model = UserInfo
        fields = '__all__'


class PetSerializer(serializers.ModelSerializer):
    pet_user = serializers.ReadOnlyField(source = 'pet_user.nickname')
    pet_image = serializers.ImageField(use_url=True, required=False, allow_empty_file=True)
    
    class Meta:
        model = PetInfo
        fields = '__all__'