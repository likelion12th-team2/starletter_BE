from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RegisterViewSet, LoginViewSet, MyPetViewSet

pet_router = SimpleRouter()
pet_router.register('pets', MyPetViewSet, basename='pets')

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post':'create'})),
    path('login/', LoginViewSet.as_view()),
    path('', include(pet_router.urls)),
]