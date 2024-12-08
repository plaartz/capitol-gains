# pylint: disable=duplicate-code, too-many-function-args
from core.controllers.SearchController import get_transactions
from django.test import TestCase


class TestSearchController(TestCase):
    """
    Tests the functionality of our search controller
    """

    fixtures = [
        "core/controllers/tests/fixtures/search.json"
    ]

    def test_get_transactions_with_last_name(self):
        """
        Tests if we get correct results when user provides
        only the last name part
        """

        transaction_data, size = get_transactions(
            "Anderson",
            "",
            False, False,
            0, 1000000000,
            False, False, False,
            "", "",
            1,
            100,
            None,
            None
        )

        assert size == 4
        for transaction in transaction_data:
            assert "Anderson" in transaction["full_name"]


    def test_get_transactions_with_first_name(self):
        """
        Tests if we get correct results when user provides
        only the first name part
        """

        transaction_data, size = get_transactions(
            "Chris",
            "",
            False, False,
            0, 1000000000,
            False, False, False,
            "", "",
            1, 100
        )

        assert size == 4
        for transaction in transaction_data:
            assert "Chris" in transaction["full_name"]


    def test_get_transactions_with_full_name(self):
        """
        Tests if we get correct results when user provides first and last name
        """

        transaction_data, size = get_transactions(
            "Daven C. Thakkar",
            "",
            False, False,
            0, 1000000000,
            False, False, False,
            "", "",
            1,
            100,
        )

        assert size == 8
        for transaction in transaction_data:
            assert "Daven C. Thakkar" in transaction["full_name"]


    def test_get_transactions_with_dates_filtered(self):
        """
        Tests if we get correct results when user provides the start and end dates
        """

        transaction_data, size = get_transactions(
            "", "",
            False, False,
            0, 1000000000,
            False, False, False,
            "2024/10/01",
            "2024/10/30",
            1,
            100,
            None,
            None
        )

        assert size == 12
        assert transaction_data is not None


    def test_get_transactions_with_end_date_filtered(self):
        """
        Tests if we get correct results when user provides only the end date
        """

        transaction_data, size = get_transactions(
            "", "",
            False, False,
            0, 1000000000,
            False, False, False,
            "",
            "2024/10/30",
            1,
            100,
            None,
            None
        )

        assert size == 22
        assert transaction_data is not None


    def test_get_transactions_with_invalid_page_number_filtered(self):
        """
        Tests if we get correct results when user provides invalid page number
        """

        transaction_data, size = get_transactions(
            "", "",
            False, False,
            0, 1000000000,
            False, False, False,
            "", "", 0, 100, None, None)

        assert size == 22
        assert transaction_data is not None


    def test_get_transactions_with_invalid_page_size_filtered(self):
        """
        Tests if we get correct results when user provides invalid page size
        """

        transaction_data, size = get_transactions(
            "", "",
            False, False,
            0, 1000000000,
            False, False, False,
            "", "", 1, 101, None, None)

        assert size == 22
        assert transaction_data is not None


    def test_get_transactions_with_stock_ticker(self):
        """
        Tests if we get correct results when user provides a stock ticker
        """
        transaction_data, size = get_transactions(
            "",
            "AAPL", 
            False, False,
            0, 1000000000,
            False, False, False,
            "", "",
            1,
            100,
            "",
            "",
            ""
        )

        assert size == 4
        for transaction in transaction_data:
            assert transaction["stock_ticker"] == "AAPL"


    def test_get_transactions_with_is_purchase(self):
        """
        Tests if we get correct results when user provides is_purchase as True
        """
        transaction_data, size = get_transactions(
            "", 
            "", 
            True, False,
            0, 1000000000,
            False, False, False,
            "", "",
            1,
            100,
            "", 
            "",
            ""
        )

        assert size == 11
        for transaction in transaction_data:
            assert transaction["transaction_type"] == "Purchase"


    def test_get_transactions_with_is_sale(self):
        """
        Tests if we get correct results when user provides is_sale as True
        """
        transaction_data, size = get_transactions(
            "", 
            "", 
            False, True,
            0, 1000000000,
            False, False, False,
            "", "",
            1,
            100,
            "", 
            "",
            ""
        )

        assert size == 11
        for transaction in transaction_data:
            assert transaction["transaction_type"] == "Sale"


    def test_get_transactions_with_price_range(self):
        """
        Tests if we get correct results when user provides a price range (min_price, max_price)
        """
        transaction_data, size = get_transactions(
            "", 
            "", 
            False, False,
            1000, 5000,
            False, False, False,
            "", "",
            1,
            100,
            "",
            "",
            ""
        )

        assert size == 8
        for transaction in transaction_data:
            assert 1000 <= int(transaction["transaction_amount"]) <= 5000


    def test_get_transactions_with_positive_gain(self):
        """
        Tests if we get correct results when user provides positive_gain as True
        """
        _, size = get_transactions(
            "", 
            "", 
            False, False,
            0, 1000000000,
            True, False, False,
            "", "",
            1,
            100,
            "",
            "",
            ""
        )

        assert size == 9


    def test_get_transactions_with_negative_gain(self):
        """
        Tests if we get correct results when user provides negative_gain as True
        """
        _, size = get_transactions(
            "", 
            "", 
            False, False,
            0, 1000000000,
            False, True, False,
            "", "",
            1,
            100,
            "", 
            "", 
            ""
        )
        assert size == 2


    def test_get_transactions_with_no_gain(self):
        """
        Tests if we get correct results when user provides no_gain as True
        """
        _, size = get_transactions(
            "", 
            "", 
            False, False,
            0, 1000000000,
            False, False, True,
            "", "",
            1,
            100,
            "", 
            "", 
            ""
        )
        assert size == 11


    def test_get_transactions_with_multiple_filters(self):
        """
        Tests if we get correct results when user applies multiple filters
        """
        _, size = get_transactions(
            "", 
            "AAPL", 
            True, False,
            1000, 5000,
            True, False, False,
            "", "",
            1,
            100,
            "", 
            "",
            ""
        )

        assert size == 0
