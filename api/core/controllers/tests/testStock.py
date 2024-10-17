from django.test import TestCase
from core.controllers import stock
from core.models import Transaction
from unittest.mock import patch
import pytest
from freezegun import freeze_time
from datetime import datetime

class TestStockController(TestCase):
    fixtures = ['core/controllers/tests/fixtures/stock.json']

    def test_get_stocks_to_update_none_found_over_one(self):
       
        stocks_to_update = stock.get_stocks_to_update()
        for _stock in stocks_to_update[0]:
            assert _stock["date_range"] == 1
        assert len(stocks_to_update[0]) == 1

        assert stocks_to_update[1] == 200

    def test_get_stocks_to_update_more_than_one_for_a_stock(self):
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
        print(stocks_to_update)
        assert len(stocks_to_update[0]) == 1 
        for item in stocks_to_update[0]:
            assert item["date_range"] == (
                datetime.now().date() - datetime.strptime("2024-01-02","%Y-%m-%d").date()).days
        assert stocks_to_update[1] == 200

    def test_get_stocks_to_update_success(self):
        Transaction.objects.create(
            politician_id=1,
            stock_id=1,
            transaction_amount="1000",
            transaction_date="2024-01-02",
            disclosure_date="2024-06-01",
            transaction_type="Purchase"
        )

        stocks_to_update = stock.get_stocks_to_update()
        print(stocks_to_update)
        assert len(stocks_to_update[0]) == 1 
        for item in stocks_to_update[0]:
            assert item["date_range"] == (
                datetime.now().date() - datetime.strptime("2024-01-02","%Y-%m-%d").date()).days
        assert stocks_to_update[1] == 200
