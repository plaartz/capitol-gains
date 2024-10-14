import pytest
from django.core.management import call_command
from ..api.core.models import StockPrice, Stock, Politician, Profile, Transaction

@pytest.fixture
@pytest.mark.django_db
def stock_price_test(django_db_setup, django_db_blocker):
    stock_prices = StockPrice.objects
    assert stock_prices.count() == 35


@pytest.fixture
@pytest.mark.django_db
def stock_test(django_db_setup, django_db_blocker):
    stocks = Stock.objects
    assert stocks.count() == 7


@pytest.fixture
@pytest.mark.django_db
def politician_test(django_db_setup, django_db_blocker):
    politicians = Politician.objects
    assert politicians.count() == 4


@pytest.fixture
@pytest.mark.django_db
def profile_test(django_db_setup, django_db_blocker):
    profiles = Profile.objects
    assert profiles.count() == 4
    assert profiles[0]['pk'] == 1
    assert profiles[0]['fields']['first_name'] == 'Daven'
    assert profiles[0]['fields']['last_name'] == 'Thakkar'
    assert profiles[0]['fields']['middle_initial'] == 'C'


@pytest.fixture
@pytest.mark.django_db
def transaction_test(django_db_setup, django_db_blocker):
    transactions = Transaction.objects
    assert transactions.count() == 22