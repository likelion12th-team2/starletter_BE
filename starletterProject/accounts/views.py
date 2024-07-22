from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PetInfo, UserInfo
from .serializers import RegisterSerializer, UserInfoSerializer, PetSerializer
from books.models import Note
from books.serializers import BookSerializer, NoteSerializer


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
    

class MyInfoViewSet(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        userinfo = UserInfo.objects.get(user=user)
        serializer = UserInfoSerializer(userinfo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = self.request.user
        userinfo = UserInfo.objects.get(user=user)
        serializer = UserInfoSerializer(userinfo, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error_message':'이미 사용 중인 닉네임입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class MyPetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PetInfo.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self, **kwargs):
        pet_user = self.request.user.userinfo
        return self.queryset.filter(pet_user=pet_user)
    
    def perform_create(self, serializer):
        pet_user = self.request.user.userinfo
        serializer.save(pet_user=pet_user)

    def perform_update(self, serializer):
        if 'pet_image' in self.request.data and self.request.data['pet_image'] == '':
            instance = serializer.instance
            instance.pet_image.delete(save=False)
            serializer.validated_data['pet_image'] = None
        pet_user = self.request.user.userinfo
        serializer.save(pet_user=pet_user)


class MyActivityView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        userinfo = self.request.user.userinfo
        books = userinfo.mind_books.all()
        book_serializer = BookSerializer(books, many=True, context={'request': request})
        notes = Note.objects.filter(author=userinfo).order_by('-id')
        note_serializer = NoteSerializer(notes, many=True)
        return Response({
                'mind_books': book_serializer.data,
                'my_notes': note_serializer.data
            }, status=status.HTTP_200_OK)

    def delete(self, request):
        note = Note.objects.get(id=request.data['note_id'])
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)