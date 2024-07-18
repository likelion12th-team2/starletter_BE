from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated

from .models import PetInfo
from .serializers import RegisterSerializer, PetSerializer


class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user, user_info = serializer.save()
            return Response({
                'username': user.username,
                'password': user.password
            }, status=status.HTTP_201_CREATED)
        else:
            error_dict = dict(serializer.errors)
            print(error_dict)
            if ('username' in error_dict) and ('nickname' in error_dict):
                error_message = '이미 사용 중인 아이디와 닉네임입니다.'
                return Response({'option':1, 'message':error_message}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in error_dict:
                error_message = '이미 사용 중인 아이디입니다.'
                return Response({'option':2, 'message':error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                error_message = '이미 사용 중인 닉네임입니다.'
                return Response({'option':3, 'message':error_message}, status=status.HTTP_400_BAD_REQUEST)
    

class MyPetViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PetInfo.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self, **kwargs):
        pet_user = self.request.user.userinfo
        return self.queryset.filter(pet_user=pet_user)
    
    def perform_create(self, serializer):
        pet_user = self.request.user.userinfo
        serializer.save(pet_user=pet_user)