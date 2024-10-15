from rest_framework import serializers
from core.models import Transaction, StockPrice
from .PoliticianSerializer import PoliticianSerializer
from .StockSerializer import StockSerializer
from .StockPriceSerializer import StockPriceSerializer

class TransactionSerializer(serializers.ModelSerializer):
    politician = PoliticianSerializer()
    stock = StockSerializer()
    stock_price = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('transaction_amount', 'transaction_date', 'disclosure_date', 'transaction_type', 'politician', 'stock', 'stock_price')

    def get_stock_price(self, obj):
        stock_price = StockPrice.objects.filter(date = obj.transaction_date, stock = obj.stock)
        stock_price_serialized = StockPriceSerializer(stock_price, many = True)
        return stock_price_serialized.data