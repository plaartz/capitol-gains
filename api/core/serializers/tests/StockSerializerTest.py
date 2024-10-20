import pytest
from core.models import Stock
from core.serializers import StockSerializer

def test_serialize_stock_price(db):
    # Create stock
    stock = Stock.objects.create(ticker = "NKE", name = "Nike", description_short = "Sports company.")

    stock_serialized = StockSerializer(stock)
    serialized_data = stock_serialized.data

    assert serialized_data['ticker'] == 'NKE'
    assert serialized_data['name'] == 'Nike'
    assert serialized_data['description_short'] == 'Sports company.'


