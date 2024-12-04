# pylint: disable=duplicate-code
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
        Tests if we get correct results when user provides only the last name
        """

        transaction_data, size = get_transactions(
            "",
            "Anderson",
            "",
            False, False,
            False, False, False,
            "", "",
            1,
            100,
            None,
            None
        )

        assert size == 4
        for transaction in transaction_data:
            assert transaction["full_name"] == "Chris L. Anderson"


    def test_get_transactions_with_first_name(self):
        """
        Tests if we get correct results when user provides only the first name
        """

        transaction_data, size = get_transactions(
            "Chris", 
            "",
            "",
            False, False,
            False, False, False,
            "", "",
            1, 100
        )

        assert size == 4
        for transaction in transaction_data:
            assert transaction["full_name"] == "Chris L. Anderson"


    def test_get_transactions_with_first_and_last_name_filtered(self):
        """
        Tests if we get correct results when user provides first and last name
        """

        transaction_data, size = get_transactions(
            "Daven",
            "Thakkar",
            "",
            False, False,
            False, False, False,
            "", "",
            1,
            100,
        )

        assert size == 8
        for transaction in transaction_data:
            assert transaction["full_name"] == "Daven C. Thakkar"


    def test_get_transactions_with_dates_filtered(self):
        """
        Tests if we get correct results when user provides the start and end dates
        """

        transaction_data, size = get_transactions(
            "", "", "",
            False, False,
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
            "", "", "",
            False, False,
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
            "", "", "",
            False, False,
            False, False, False,
            "", "", 0, 100, None, None)

        assert size == 22
        assert transaction_data is not None


    def test_get_transactions_with_invalid_page_size_filtered(self):
        """
        Tests if we get correct results when user provides invalid page size
        """

        transaction_data, size = get_transactions(
            "", "", "",
            False, False,
            False, False, False,
            "", "", 1, 101, None, None)

        assert size == 22
        assert transaction_data is not None
