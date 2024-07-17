from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import RegisterViewSet, LoginViewSet, PetViewSet

pet_router = SimpleRouter(trailing_slash=False)
pet_router.register('pets', PetViewSet, basename='pet')

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post':'create'})),
    path('login/', LoginViewSet.as_view()),
    path('', include(pet_router.urls)),
]