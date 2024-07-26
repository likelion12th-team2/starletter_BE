from django.urls import path, include
from .views import MarketViewSet
from rest_framework.routers import SimpleRouter 

router = SimpleRouter()
router.register('', MarketViewSet, basename='market')

urlpatterns = [
    path('', include(router.urls)),
]