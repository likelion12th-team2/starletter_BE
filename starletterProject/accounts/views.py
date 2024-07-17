from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet 
from .serializers import RegisterSerializer, LoginSerializer

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
    

class PetViewSet(ModelViewSet):
    queryset = PetInfo.objects.all()
    serializer_class = PetSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)