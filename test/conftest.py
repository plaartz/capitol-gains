import pytest
from django.core.management import call_command
from ..api.core.models import StockPrice, Stock, Politician, Profile, Transaction

@pytest.fixture
def stock_price_test():
    stock_prices = StockPrice.objects
    assert stock_prices.count() == 35


@pytest.fixture
def stock_test():
    stocks = Stock.objects
    assert stocks.count() == 7


@pytest.fixture
def politician_test():
    politicians = Politician.objects
    assert politicians.count() == 4


@pytest.fixture
def profile_test():
    profiles = Profile.objects
    assert profiles.count() == 4
    assert profiles[0]['pk'] == 1
    assert profiles[0]['fields']['first_name'] == 'Daven'
    assert profiles[0]['fields']['last_name'] == 'Thakkar'
    assert profiles[0]['fields']['middle_initial'] == 'C'


@pytest.fixture
def transaction_test():
    transactions = Transaction.objects
    assert transactions.count() == 22