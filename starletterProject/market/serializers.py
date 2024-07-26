from rest_framework import serializers
from .models import Market

class MarketSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    class Meta:
        model = Market
        fields = '__all__'