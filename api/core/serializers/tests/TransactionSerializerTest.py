import pytest
from core.models import *
from core.serializers import TransactionSerializer

def test_serialize_stock_price(db):
    # Create stock
    stock = Stock.objects.create(ticker = "NKE", name = "Nike", description_short = "Sports company.")
    # Create stock price
    StockPrice.objects.create(stock = stock, price = 82.79, date = "2024-08-28")
    # Create profile
    profile = Profile.objects.create(first_name = "Daven", last_name = "Thakkar", middle_initial = "C")
    # Create politician 
    politician = Politician.objects.create(profile = profile, politician_type = "Senate", politician_house = "I")
    # Create transaction
    transaction = Transaction.objects.create(politician = politician, stock = stock, transaction_amount = "1000", transaction_date = "2024-08-28", disclosure_date = "2024-09-05", transaction_type = "Purchase")

    transaction_serialized = TransactionSerializer(transaction)
    serialized_data = transaction_serialized.data

    assert serialized_data['transaction_amount'] == '1000'
    assert serialized_data['transaction_date'] == '2024-08-28'
    assert serialized_data['disclosure_date'] == '2024-09-05'
    assert serialized_data['transaction_type'] == 'Purchase'
    assert serialized_data['full_name'] == 'Daven C. Thakkar'
    assert serialized_data['politician_type'] == 'Senate'
    assert serialized_data['politician_house'] == 'I'
    assert serialized_data['stock_ticker'] == 'NKE'
    assert serialized_data['stock_price'] == 82.79
    assert serialized_data['stock_description'] == 'Sports company.'


