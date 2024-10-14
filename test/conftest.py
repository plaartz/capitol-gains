import pytest
from django.core.management import call_command
from ..api.core.models import StockPrice, Stock

@pytest.fixture
@pytest.mark.django_db
def stock_price_test(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'api/api/fixtures/StockPriceFixture.json')
    stocks_without_prices = StockPrice.objects
    assert stocks_without_prices.count() == 35

@pytest.fixture
@pytest.mark.django_db
def stock_test(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'api/api/fixtures/StockFixture.json')
    stocks = Stock.objects
    assert stocks.count() == 7