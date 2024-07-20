from django.urls import path, include
from .views import FnrHallViewSet
from rest_framework.routers import SimpleRouter 

router = SimpleRouter()
router.register('', FnrHallViewSet, basename='funeralhalls')

urlpatterns = [
    path('', include(router.urls)),
]