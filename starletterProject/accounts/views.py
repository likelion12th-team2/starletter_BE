from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet 
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user, user_info = serializer.save()
            return Response({
                'username': user.username,
                'password': user.password
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    

class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data 
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    

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