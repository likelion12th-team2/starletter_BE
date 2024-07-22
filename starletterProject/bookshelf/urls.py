from django.urls import path, include
from .views import *


urlpatterns = [
    path('', BookShelfView.as_view()),
    path('<int:pk>/', BookPageView.as_view()),
    path('<int:pk>/mind/', MindView.as_view()),
]