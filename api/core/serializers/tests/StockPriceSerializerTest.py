import pytest
from core.models import StockPrice, Stock
from core.serializers import StockPriceSerializer

def test_serialize_stock_price(db):
    # Create stock
    stock = Stock.objects.create(ticker = "NKE", name = "Nike", description_short = "Sports company.")
    # Create stock price
    stock_price = StockPrice.objects.create(stock = stock, price = 82.97, date = "2024-10-01")

    stock_price_serialized = StockPriceSerializer(stock_price)
    serialized_data = stock_price_serialized.data

    assert serialized_data['price'] == 82.97
    assert serialized_data['date'] == '2024-10-01'
    assert serialized_data['stock']['ticker'] == 'NKE'
    assert serialized_data['stock']['name'] == 'Nike'
    assert serialized_data['stock']['description_short'] == 'Sports company.'


