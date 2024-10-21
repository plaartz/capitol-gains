# pylint: disable=missing-class-docstring, too-few-public-methods
from rest_framework import serializers
from core.models import Stock

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('ticker', 'name', 'description_short')
