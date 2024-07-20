from django.shortcuts import render
from rest_framework import viewsets, filters

from .models import FuneralHall
from .serializers import FuneralHallSerializer


class FnrHallViewSet(viewsets.ModelViewSet):
    queryset = FuneralHall.objects.all()
    serializer_class = FuneralHallSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location', 'tag']
