from django.shortcuts import render
from django.db.models import Q, Count, Exists, OuterRef
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from books.models import Book, Page, Note
from books.serializers import *

# Create your views here.


class BookShelfView(APIView):
    def get(self, request):
        if self.request.query_params: # 검색한 경우
            queryset = Book.objects.annotate(
                has_public_pages=Exists(Page.objects.filter(book=OuterRef('id'), is_public=True))
            ).filter(has_public_pages=True)

            search_keyword = self.request.GET['search']
            words = search_keyword.split(' ')
            queryset = queryset.filter(
                Q(author__nickname__icontains=words[0]) | Q(keyword_tag__icontains=words[0]) 
                | Q(title__icontains=words[0]) | Q(pet__pet_type__icontains=words[0])
            )
            for word in words[1:]:
                queryset = queryset.filter(
                    Q(author__nickname__icontains=word) | Q(keyword_tag__icontains=word) 
                    | Q(title__icontains=word) | Q(pet__pet_type__icontains=word)
                )

            queryset = queryset.distinct()
            serializer = BookSerializer(queryset, many=True, context={'request': request})
            return Response({'searched_books': serializer.data}, status=status.HTTP_200_OK)
        
        else: # 검색하지 않은 경우 
            queryset = Book.objects.annotate(
                has_public_pages=Exists(Page.objects.filter(book=OuterRef('id'), is_public=True))
            ).filter(has_public_pages=True)
            
            books_most_minds = queryset.annotate(minds=Count('mind')).order_by('-minds')[:5]
            books_recent = queryset.order_by('-last_updated')[:5]

            bmm_serializer = BookSerializer(books_most_minds, many=True, context={'request': request})
            br_serializer = BookSerializer(books_recent, many=True, context={'request': request})

            return Response({
                'books_most_minds': bmm_serializer.data,
                'books_recent': br_serializer.data
            }, status=status.HTTP_200_OK)
    

class BookPageView(APIView):
    def get_permissions(self):
        if self.request.method == 'post': # 포스트잇 POST에만 로그인 요구, GET은 비로그인 이용가능
            return [IsAuthenticated()] 
        return []
    
    def get(self, request, pk): # 책 개별 조회
        if self.request.user.is_authenticated:
            userinfo = self.request.user.userinfo
        else:
            userinfo = AnonymousUser
        book = Book.objects.get(id=pk)
        
        pages = Page.objects.filter(book=book)
        if userinfo == AnonymousUser or userinfo != book.author: # 비밀페이지 필터링
            pages = pages.filter(is_public=True)
        pages_serializer = PageSerializer(pages, many=True, context={'request': request})

        notes = Note.objects.filter(book=book)
        notes_serializer = NoteSerializer(notes, many=True)

        if userinfo == AnonymousUser:
            is_minded = False
        else:
            is_minded = userinfo in book.mind.all()

        return Response({
            'pages': pages_serializer.data,
            'notes': notes_serializer.data,
            'is_minded': is_minded
        }, status=status.HTTP_200_OK)
    
    def post(self, request, pk): # 포스트잇 POST
        book = Book.objects.get(id=pk)
        author = self.request.user.userinfo
        note_serializer = NoteSerializer(data=request.data)
        if note_serializer.is_valid():
            note_serializer.save(
                book=book,
                author=author,
            )
            return Response(note_serializer.data, status=status.HTTP_201_CREATED)
        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MindView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        userinfo = self.request.user.userinfo
        if userinfo == book.author:
            message = '본인의 책은 공감할 수 없어요'
            return Response({'option':3, 'message':message}, status=status.HTTP_400_BAD_REQUEST)
        elif userinfo in book.mind.all():
            book.mind.remove(userinfo)
            message = '공감을 취소했습니다'
            return Response({'option':2, 'message':message}, status=status.HTTP_200_OK)
        else:
            book.mind.add(userinfo)
            message = '공감했습니다'
            return Response({'option':1, 'message':message}, status=status.HTTP_200_OK)
