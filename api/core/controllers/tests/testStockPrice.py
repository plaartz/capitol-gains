from datetime import datetime
from django.test import TestCase
from core.controllers import stock
from core.models import Transaction, StockPrice, Stock

class TestStockPriceController(TestCase):
    """
    Tests the functionality of our stock price controller
    """
    fixtures = ['core/controllers/tests/fixtures/stock.json']

    def setUp(self):
        self.stock1 = Stock.objects.create(ticker='AAPL', name='Apple Inc.', description_short='Some Tech company')
        self.stock2 = Stock.objects.create(ticker='TSLA', name='Tesla Inc.', description_short='Electric cars')

    def test_upload_valid_data(self):
        valid_data = {
            'AAPL': {
                'prices': {
                    'price': 150.0,
                    'date': '2024-10-22'
                }
            },
            'TSLA': {
                'prices': {
                    'price': 700.5,
                    'date': '2024-10-21'
                }
            }
        }
        status_code = stock.upload_stock_prices(valid_data)
        self.assertEqual(status_code, 200)
        
        apple_price = StockPrice.objects.get(stock=self.stock1)
        tesla_price = StockPrice.objects.get(stock=self.stock2)
        self.assertEqual(apple_price.price, 150.0)
        self.assertEqual(apple_price.date, '2024-10-22')
        self.assertEqual(tesla_price.price, 700.5)
        self.assertEqual(tesla_price.date, '2024-10-21')

    def test_upload_invalid_price(self):
        invalid_data = {
            'AAPL': {
                'prices': {
                    'price': -50.00,
                    'date': '2024-10-22'
                }
            }
        }
        status_code = stock.upload_stock_prices(invalid_data)
        self.assertEqual(status_code, 400)

    def test_upload_missing_price_key(self):
        missing_price_data = {
            'AAPL': {
                'prices': {
                    'date': '2024-10-22'
                }
            }
        }
        status_code = stock.upload_stock_prices(missing_price_data)
        self.assertEqual(status_code, 400)

    def test_upload_new_stock_price_for_new_stock(self):
        new_price_data = {
            'META': {
                'prices': {
                    'price': 160.50,
                    'date': '2024-10-22',
                }
            }
        }
        status_code = stock.upload_stock_prices(new_price_data)
        self.assertEqual(status_code, 200)
        stock = StockPrice.objects.get()

    def test_upload_data_to_update_existing_entry(self):
        conflicting_data = {
            'AAPL': {
                'prices': {
                    'price': 170.0,
                    'date': '2024-10-22'
                }
            }
        }
        status_code = stock.upload_stock_prices(conflicting_data)
        self.assertEqual(status_code, 200)

        status_code = stock.upload_stock_prices(conflicting_data)
        self.assertEqual(status_code, 200)


