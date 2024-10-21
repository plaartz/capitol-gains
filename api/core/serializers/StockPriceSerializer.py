# pylint: disable=missing-class-docstring, too-few-public-methods
from rest_framework import serializers
from core.models import StockPrice
from .StockSerializer import StockSerializer

class StockPriceSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = StockPrice
        fields = ('stock', 'price', 'date')
