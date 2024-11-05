from datetime import datetime

from django.test import TestCase
from core.controllers import stock
from core.models import Transaction

def is_weekday():
    """ 
    Checks whether it's a weekday 
    
    @return     true if it's a weekday, false otherwise
    """
    today = datetime.now().date()
    return today.weekday() < 5

class TestStockController(TestCase):
    """
    Tests the functionality of our stock controllers
    """
    fixtures = ['core/controllers/tests/fixtures/stock.json']

    def test_get_stocks_to_update_none_found_over_one(self):
        """ 
        Tests that we only get 1-3 date range if its a weekday or not.
        """

        stocks_to_update = stock.get_stocks_to_update()
        for item in stocks_to_update[0]:
            if is_weekday():
                assert item["date_range"] == 1
            else:
                assert item["date_range"] == 2 or item["date_range"] == 3
        assert len(stocks_to_update[0]) == 1

        assert stocks_to_update[1] == 200

    def test_get_stocks_to_update_more_than_one_for_a_stock(self):
        """ 
        Tests that if we have more than one missing date for a transaction, 
        we fetch the oldest. 
        """

        Transaction.objects.create(
            politician_id=1,
            stock_id=1,
            transaction_amount="1000",
            transaction_date="2024-01-02",
            disclosure_date="2024-06-01",
            transaction_type="Purchase"
        )
        Transaction.objects.create(
            politician_id=1,
            stock_id=1,
            transaction_amount="1000",
            transaction_date="2024-02-02",
            disclosure_date="2024-06-01",
            transaction_type="Purchase"
        )

        stocks_to_update = stock.get_stocks_to_update()

        assert len(stocks_to_update[0]) == 1
        for item in stocks_to_update[0]:
            assert item["date_range"] == (
                datetime.now().date() - datetime.strptime("2024-01-02","%Y-%m-%d").date()).days + 1
        assert stocks_to_update[1] == 200

    def test_get_stocks_to_update_success(self):
        """ Tests that it functions with just 1 missing stock price. """

        Transaction.objects.create(
            politician_id=1,
            stock_id=1,
            transaction_amount="1000",
            transaction_date="2024-01-02",
            disclosure_date="2024-06-01",
            transaction_type="Purchase"
        )

        stocks_to_update = stock.get_stocks_to_update()

        assert len(stocks_to_update[0]) == 1
        for item in stocks_to_update[0]:
            assert item["date_range"] == (
                datetime.now().date() - datetime.strptime("2024-01-02","%Y-%m-%d").date()).days + 1
        assert stocks_to_update[1] == 200
