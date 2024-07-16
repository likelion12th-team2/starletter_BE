from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .models import UserInfo

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
    password2 = serializers.CharField(write_only=True, required=True) # 비밀번호 재확인 
    name = serializers.CharField(max_length=30, required=True)
    nickname = serializers.CharField(
        max_length=100,
        required=True,
        validators=[UniqueValidator(queryset=UserInfo.objects.all())], # 닉네임 중복확인
    )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        token = Token.objects.create(user=user)
        user_info = UserInfo.objects.create(
            user=user,
            name=validated_data['name'],
            nickname=validated_data['nickname']
        )
        return user, user_info