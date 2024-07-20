from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q

from .models import FuneralHall
from .serializers import FuneralHallSerializer


class FnrHallViewSet(viewsets.ModelViewSet):
    queryset = FuneralHall.objects.all()
    serializer_class = FuneralHallSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location', 'tag']

    def get_queryset(self):
        return self.queryset.filter(Q(location__contains='경기') | Q(location__contains='인천')).order_by("?")[:3]
        # 수도권 랜덤으로 3개씩 
