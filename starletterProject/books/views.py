from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from accounts.serializers import *


# 내 서재 (기본)
@api_view(['GET'])
def MyBook(request):
    pet = PetInfo.objects.filter(pet_user=request.user)
    book = Book.objects.filter(user=request.user)

    # 반려동물 X 경우
    if not pet.exists():
        return redirect('MyBookAddPet/') # MyBookAddPet로 리다이렉트
    
    # 반려동물 O, 책 X 경우
    elif not book.exists():
        return redirect('MyBookMake/') # MyBookMake로 리다이렉트
    
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data)

# 내 서재 - 반려동물 X 경우 ->  Pet 등록
@api_view(['POST'])
def MyBookAddPet(request):
    serializer = PetSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=404)

# 내 서재 - 책 X 경우
@api_view(['GET', 'POST'])
def MyBookMake(request):
    if request.method == 'GET':
        pet = PetInfo.objects.all()
        serializer = PetSerializer(pet, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)
        

# 내 서재 - Detail
@api_view(['GET'])
def MyBookDetail(request, pk):
    try:
        books = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    books_serializer = BookSerializer(books, many=True)

    pages = Page.objects.filter(book = books)
    pages_serializer = PageSerializer(pages, many=True)

    notes = Note.objects.filter(book = books)
    notes_serializer = NoteSerializer(notes, many=True)

    return Response(books_serializer, pages_serializer, notes_serializer)

# 내 서재 - 새 페이지 쓰기
@api_view(['POST'])
def MyBookWrite(request):
    serializer = PageSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=404)



'''
class MyBook(APIView): 
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save(author = self.request.user) # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제하기
    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
    


# book 목록
class BookList(APIView):
    # book 목록 보여주기
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    # 공감 많이 받은 책
    # 이주의 책
    # 검색

# 책방 책 (book detail)
class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all().order_by('created_at')
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user)

    def get_queryset(self, **kwargs):
        id = self.kwargs['book_id']
        return self.queryset.filter(book=id)


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all().order_by('created_at')
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    def get_queryset(self, **kwargs):
        id = self.kwargs['book_id']
        return self.queryset.filter(book=id)
'''    

# 공감하기 목록
class MindView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookMindSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if request.user in book.minds.all():
            book.minds.remove(request.user)
            return Response("취소하기", status=status.HTTP_200_OK)
        else:
            book.minds.add(request.user)
            return Response("공감하기", status=status.HTTP_200_OK)
