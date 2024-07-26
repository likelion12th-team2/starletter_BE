from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q

from .models import Market
from .serializers import MarketSerializer


class MarketViewSet(viewsets.ModelViewSet):

    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get_queryset(self):
        return self.queryset.all().order_by("?")[:6]
        # 랜덤으로 6개씩 
