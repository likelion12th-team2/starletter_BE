from rest_framework import serializers
from .models import FuneralHall

class FuneralHallSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = FuneralHall
        fields = '__all__'