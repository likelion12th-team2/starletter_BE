from django.shortcuts import render, redirect

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.models import PetInfo
from accounts.serializers import PetSerializer
from .models import *
from .serializers import *


class MyBookMainView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        userinfo = self.request.user.userinfo
        my_pets = PetInfo.objects.filter(pet_user=userinfo)
        if my_pets.exists():
            return redirect('list/')
        return redirect('no-pets/')
    

class MyBookNoPetView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, reqeust):
        return Response(status=status.HTTP_204_NO_CONTENT)
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        pet_user = self.request.user.userinfo
        if serializer.is_valid(): 
            serializer.save(pet_user=pet_user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MyBookListView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userinfo = self.request.user.userinfo
        my_pets = PetInfo.objects.filter(pet_user=userinfo)

        pets_with_book = my_pets.filter(pet_book__isnull=False)
        pet_books = [pet.pet_book for pet in pets_with_book]
        pets_no_book = my_pets.filter(pet_book__isnull=True)

        with_serializer = BookSerializer(pet_books, many=True)
        no_serializer = PetSerializer(pets_no_book, many=True)

        return Response({
            'books': with_serializer.data,
            'pets_no_book': no_serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user.userinfo,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)