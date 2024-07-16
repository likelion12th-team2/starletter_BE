from django.urls import path
from .views import RegisterViewSet, LoginViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post':'create'})),
    path('login/', LoginViewSet.as_view()),
]