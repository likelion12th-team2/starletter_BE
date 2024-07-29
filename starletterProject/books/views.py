from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from datetime import datetime
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
        serializer = PetSerializer(data=request.data, context={'request': request})
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

        with_serializer = BookSerializer(pet_books, many=True, context={'request': request})
        no_serializer = PetSerializer(pets_no_book, many=True, context={'request': request})

        return Response({
            'books': with_serializer.data,
            'pets_no_book': no_serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                author=self.request.user.userinfo,
                last_updated=datetime.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 내 서재 - Detail (페이지 + 포스트잇 GET, 새 페이지 POST)
class MyBookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        book_serializer = BookSerializer(book, context={'request': request})

        pages = Page.objects.filter(book=book)
        pages_serializer = PageSerializer(pages, many=True, context={'request': request})

        notes = Note.objects.filter(book=book)
        notes_serializer = NoteSerializer(notes, many=True)

        return Response({
            'book': book_serializer.data,
            'pages': pages_serializer.data,
            'notes': notes_serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        page_serializer = PageSerializer(data=request.data, context={'request': request})

        if page_serializer.is_valid():
            page_serializer.save(
                book=book,
                author=self.request.user.userinfo,
                created_at=datetime.now()
            )
            book.last_updated = datetime.now()
            book.save(update_fields=['last_updated'])
            return Response(page_serializer.data, status=status.HTTP_201_CREATED)
        return Response(page_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
