from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q

from .models import FuneralHall
from .serializers import FuneralHallSerializer


class FnrHallViewSet(viewsets.ModelViewSet):
    queryset = FuneralHall.objects.all()
    serializer_class = FuneralHallSerializer

    def get_queryset(self):
        if self.request.query_params:
            search_keyword = self.request.GET['search']
            words = search_keyword.split(' ')
            queryset = self.queryset.filter(
                Q(name__icontains=words[0]) | Q(location__icontains=words[0]) | Q(tag__icontains=words[0])
            )
            for word in words[1:]:
                queryset = queryset.filter(
                    Q(name__icontains=word) | Q(location__icontains=word) | Q(tag__icontains=word)
                )
            return queryset.distinct()
        else:
            return self.queryset.filter(Q(location__contains='경기') | Q(location__contains='인천')).order_by("?")[:3]
        # 수도권 랜덤으로 3개씩 
