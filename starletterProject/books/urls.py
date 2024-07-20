from django.urls import path, include
from .views import *


urlpatterns =[
    path('', MyBookMainView.as_view()),
    path('no-pets/', MyBookNoPetView.as_view()),
    path('list/', MyBookListView.as_view()),
]