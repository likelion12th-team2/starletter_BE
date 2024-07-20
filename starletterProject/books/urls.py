from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from . import views
from .views import *

urlpatterns =[
    path('MyBook/', MyBook), # 내 서재(기본)
    path('MyBookAddPet/', MyBookAddPet), # 내 서재 - pet등록
    path('MyBookMake/', MyBookMake), # 내 서재 - 책 없을 때 책 생성
    path('MyBookDetail/', MyBookDetail), # 내 서재 - detail
    path('MyBookWrite/', MyBookWrite), # 내 서재 - 내 글 쓰기
]

urlpatterns = format_suffix_patterns(urlpatterns)