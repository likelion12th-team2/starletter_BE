from django.shortcuts import render
from rest_framework import viewsets, status
from django.db.models import Q
from rest_framework.response import Response

from rest_framework.views import APIView
from funeralhalls.models import FuneralHall
from funeralhalls.serializers import FuneralHallSerializer
from market.models import Market
from market.serializers import MarketSerializer



class IndexView(APIView):
    def get(self, request):
        # 장례식장
        funeralhalls_queryset = FuneralHall.objects.all()

        # 마켓
        market_queryset = Market.objects.all()

        market_queryset = market_queryset.all().order_by("?")[:6]

        if self.request.query_params:
            search_keyword = self.request.GET['search']
            words = search_keyword.split(' ')
            funeralhalls_queryset = self.funeralhalls_queryset.filter(
                Q(name__icontains=words[0]) | Q(location__icontains=words[0]) | Q(tag__icontains=words[0])
            )
            for word in words[1:]:
                funeralhalls_queryset = funeralhalls_queryset.filter(
                    Q(name__icontains=word) | Q(location__icontains=word) | Q(tag__icontains=word)
                )
            funeralhalls_queryset = funeralhalls_queryset.distinct()
            
        else:
            funeralhalls_queryset = funeralhalls_queryset.filter(Q(location__contains='경기') | Q(location__contains='인천')).order_by("?")[:3]
        
        funeralhalls_serializer = FuneralHallSerializer(funeralhalls_queryset, many=True, context={'request': request})
        market_serializer = MarketSerializer(market_queryset, many=True, context={'request': request})

        return Response({
            'funeralhalls_queryset': funeralhalls_serializer.data,  # 장례식장 쿼리셋 결과
            'market_queryset': market_serializer.data,  # 마켓 쿼리셋 결과
        }, status=status.HTTP_200_OK)
    