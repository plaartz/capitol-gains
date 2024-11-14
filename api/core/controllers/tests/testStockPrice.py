# pylint: disable=invalid-name
from datetime import date
from django.test import TestCase
from core.controllers import stock
from core.models import StockPrice, Stock

class TestStockPriceController(TestCase):
    """
    Tests the functionality of our stock price controller
    """

    def setUp(self):
        """
        Initializes 2 Stocks in the database
        """
        self.stock1 = Stock.objects.create(
            ticker='AAPL',
            name='Apple Inc.',
            description_short='Some Tech company'
        )
        self.stock2 = Stock.objects.create(
            ticker='TSLA',
            name='Tesla Inc.',
            description_short='Electric cars'
        )

    def test_upload_valid_data(self):
        """
        Tests that two valid stock price objects are able to be uploaded successfully
        """
        valid_data = {
            'AAPL': {
                'prices': [
                    {
                        'price': 150.0,
                        'date': '2024-10-22'
                    },
                    {
                        'price': 175.0,
                        'date': '2024-10-23'
                    }
                ]
            },
            'TSLA': {
                'prices': [
                    {
                        'price': 700.5,
                        'date': '2024-10-21'
                    }
                ]
            }
        }
        status_code = stock.upload_stock_prices(valid_data)
        self.assertEqual(status_code, 200)

        apple_prices = StockPrice.objects.filter(stock=self.stock1)
        tesla_price = StockPrice.objects.get(stock=self.stock2)
        self.assertEqual(len(apple_prices), 2)
        self.assertEqual(apple_prices[0].price, 150.0)
        self.assertEqual(apple_prices[0].date, date(2024, 10, 22))
        self.assertEqual(apple_prices[1].price, 175.0)
        self.assertEqual(apple_prices[1].date, date(2024, 10, 23))
        self.assertEqual(tesla_price.price, 700.5)
        self.assertEqual(tesla_price.date, date(2024, 10, 21))

    def test_upload_invalid_price(self):
        """
        Tests that invalid price formats don't get added
        """
        invalid_data = {
            'AAPL': {
                'prices': [
                    {
                        'price': -50.00,
                        'date': '2024-10-22'
                    }
                ]
            }
        }
        invalid_data_2 = {
            'TSLA': {
                'prices': [
                    {
                        'price': 'not a number',
                        'date': '2024-10-22'
                    }
                ]
            }
        }
        status_code = stock.upload_stock_prices(invalid_data)
        status_code_2 = stock.upload_stock_prices(invalid_data_2)
        self.assertEqual(status_code, 200)
        self.assertEqual(status_code_2, 200)
        self.assertEqual(StockPrice.objects.count(), 0)

    def test_upload_missing_price_key(self):
        """
        Tests that missing columns don't get added
        """
        missing_price_data = {
            'AAPL': {
                'prices': [
                    {
                        'date': '2024-10-22'
                    }
                ]
            }
        }
        missing_price_status_code = stock.upload_stock_prices(missing_price_data)
        self.assertEqual(missing_price_status_code, 200)
        self.assertEqual(StockPrice.objects.count(), 0)

        missing_date_data = {
            'TSLA': {
                'prices': [
                    {
                        'price': 200.0,
                    }
                ]
            }
        }
        missing_date_status_code = stock.upload_stock_prices(missing_date_data)
        self.assertEqual(missing_date_status_code, 200)
        self.assertEqual(StockPrice.objects.count(), 0)

    def test_upload_new_stock_price_for_nonexistant_stock_fail(self):
        """
        Tests that a stock price object without an existing stock doesn't get added
        """
        new_price_data = {
            'META': {
                'prices': [
                    {
                        'price': 160.50,
                        'date': '2024-10-22',
                    }
                ]
            }
        }
        status_code = stock.upload_stock_prices(new_price_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(StockPrice.objects.count(), 0)

    def test_upload_data_to_update_existing_entry(self):
        """
        Tests that prices get updated instead of creating new objects
        if the price changes on the same date
        """
        original_data = {
            'AAPL': {
                'prices': [
                    {
                        'price': 170.0,
                        'date': '2024-10-22'
                    }
                ]
            }
        }
        status_code = stock.upload_stock_prices(original_data)
        self.assertEqual(status_code, 200)
        original_apple_price = StockPrice.objects.get(stock=self.stock1)
        self.assertEqual(original_apple_price.price, 170.0)

        new_data = {
            'AAPL': {
                'prices': [
                    {
                        'price': 180.0,
                        'date': '2024-10-22'
                    }
                ]
            }
        }
        new_status_code = stock.upload_stock_prices(new_data)
        self.assertEqual(new_status_code, 200)
        different_apple_price = StockPrice.objects.get(stock=self.stock1)
        self.assertEqual(different_apple_price.price, 180.0)

        different_date_data = {
            'AAPL': {
                'prices': [
                    {
                        'price': 170.0,
                        'date': '2024-10-21'
                    }
                ]
            }
        }
        other_status_code = stock.upload_stock_prices(different_date_data)
        self.assertEqual(other_status_code, 200)
        number_of_stock_prices = StockPrice.objects.filter(stock=self.stock1).count()
        self.assertEqual(number_of_stock_prices, 2)
