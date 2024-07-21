from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RegisterViewSet, MyPetViewSet, MyInfoViewSet


pet_router = SimpleRouter()
pet_router.register('pets', MyPetViewSet, basename='pets')

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post':'create'})),
    path('', include('dj_rest_auth.urls')),
    path('myinfo/', MyInfoViewSet.as_view()),
    path('', include(pet_router.urls)),
]