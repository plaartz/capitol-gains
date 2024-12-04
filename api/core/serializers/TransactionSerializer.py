# pylint: disable=missing-class-docstring, too-few-public-methods
from rest_framework import serializers
from core.models import Transaction, StockPrice
from .StockPriceSerializer import StockPriceSerializer

class TransactionSerializer(serializers.ModelSerializer):
    stock_price = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    stock_ticker = serializers.SerializerMethodField()
    stock_description = serializers.SerializerMethodField()
    percent_gain = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'transaction_amount',
            'transaction_date',
            'disclosure_date',
            'transaction_type',
            'full_name',
            'stock_ticker',
            'stock_price',
            'percent_gain',
            'stock_description'
        )

    def get_stock_price(self, obj):
        """
        Gets the correct stock price

        @ return    returns the stock price
        """

        stock_price = StockPrice.objects.filter(
            date = obj.transaction_date,
            stock = obj.stock
        ).first()
        stock_price_serialized = StockPriceSerializer(stock_price)
        return stock_price_serialized.data['price']


    def get_full_name(self, obj):
        """
        Gets the correct name

        @ return    returns the full name of the politician 
        """

        return obj.politician.profile.full_name


    def get_stock_ticker(self, obj):
        """
        Gets the correct stock ticker

        @ return    returns the stock ticker
        """

        return obj.stock.ticker


    def get_stock_description(self, obj):
        """
        Gets the correct stock description

        @ return    returns the stock description
        """

        return obj.stock.description_short


    def get_percent_gain(self, obj):
        """
        Gets the correct stock percent gain

        @ return    returns the stock percent gain
        """

        return obj.percent_gain
