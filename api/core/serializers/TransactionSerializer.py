from rest_framework import serializers
from core.models import Transaction, StockPrice
from .PoliticianSerializer import PoliticianSerializer
from .StockSerializer import StockSerializer
from .StockPriceSerializer import StockPriceSerializer

class TransactionSerializer(serializers.ModelSerializer):
    stock_price = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    politician_type = serializers.SerializerMethodField()
    politician_house = serializers.SerializerMethodField()
    stock_ticker = serializers.SerializerMethodField()
    stock_description = serializers.SerializerMethodField()
    percent_gain = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ('transaction_amount', 'transaction_date', 'disclosure_date', 'transaction_type', 'full_name', 'politician_type', 'politician_house', 'stock_ticker', 'stock_price', 'percent_gain', 'stock_description')

    def get_stock_price(self, obj):
        stock_price = StockPrice.objects.filter(date = obj.transaction_date, stock = obj.stock).first()
        stock_price_serialized = StockPriceSerializer(stock_price)
        return stock_price_serialized.data['price']


    def get_full_name(self, obj):
        return obj.politician.profile.full_name


    def get_politician_type(self, obj):
        return obj.politician.politician_type


    def get_politician_house(self, obj):
        return obj.politician.politician_house


    def get_stock_ticker(self, obj):
        return obj.stock.ticker


    def get_stock_description(self, obj):
        return obj.stock.description_short
        
    
    def get_percent_gain(self, obj):
        return obj.percent_gain