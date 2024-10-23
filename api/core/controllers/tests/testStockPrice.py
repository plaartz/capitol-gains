from datetime import datetime

from django.test import TestCase
from core.controllers import stock
from core.models import Transaction, StockPrice, Stock

class TestStockPriceController(TestCase):
    """
    Tests the functionality of our stock price controller
    """
    fixtures = ['core/controllers/tests/fixtures/stock.json']

    def test_update_invalid_stock_price(self):
        """
        Tests should fail when trying to upload an invalid stock
        """
        Stock.objects.create(
            ticker="AAPL",
            name="Apple",
            description_short="some tech company"
        )
        StockPrice.objects.create(
            stock="AAPL",
            price=-3.00,
            date="2024-07-01"
        )
        pass

    def test_update_valid_stock_price(self):
        """
        Tests if a valid stock price was uploaded correctly
        """
        Stock.objects.create(
            ticker="AAPL",
            name="Apple",
            description_short="some tech company"
        )
        StockPrice.objects.create(
            stock="AAPL",
            price=30.00,
            date="2024-06-01"
        )
        stock_prices = StockPrice.objects.all()
        assert stock_prices.count() == 1


