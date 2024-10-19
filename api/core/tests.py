import unittest
from django.test import TestCase
from .models import StockPrice, Stock, Politician, Profile, Transaction

class StockPriceTestCase(TestCase):

    def test_stock_price_count(self):
        stock_prices = StockPrice.objects
        self.assertEqual(stock_prices.count(), 35)


class StockTestCase(TestCase):

    def test_stock_count(self):
        stocks = Stock.objects
        self.assertEqual(stocks.count(), 7)


class PoliticianTestCase(TestCase):

    def test_politician_count(self):
        politicians = Politician.objects
        self.assertEqual(politicians.count(), 4)


class ProfileTestCase(TestCase):

    def test_profile_count(self):
        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 4)

    def test_profile_fields(self):
        profile = Profile.objects.first()
        self.assertEqual(profile.pk, 1)
        self.assertEqual(profile.first_name, 'Daven')
        self.assertEqual(profile.last_name, 'Thakkar')
        self.assertEqual(profile.middle_initial, 'C')
        self.assertTrue(isinstance(profile, Profile))


class TransactionTestCase(TestCase):

    def test_transaction_count(self):
        transactions = Transaction.objects
        self.assertEqual(transactions.count(), 22)


if __name__ == '__main__':
    unittest.main()