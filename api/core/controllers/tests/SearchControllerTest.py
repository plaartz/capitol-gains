# pylint: disable=duplicate-code
from core.controllers.SearchController import get_transactions
from django.test import TestCase


class TestSearchController(TestCase):
    """
    Tests the functionality of our search controller
    """

    fixtures = [
        "api/fixtures/StockFixture.json",
        "api/fixtures/StockPriceFixture.json",
        "api/fixtures/ProfileFixture.json",
        "api/fixtures/PoliticianFixture.json",
        "api/fixtures/TransactionFixture.json"
    ]

    def test_get_transactions_with_last_name(self):
        """
        Tests if we get correct results when user provides only the last name
        """

        transaction_data, size = get_transactions("", "Anderson", "", "", "", "", 1, 100)

        assert size == 4
        for transaction in transaction_data:
            assert transaction["full_name"] == "Chris L. Anderson"


    def test_get_transactions_with_first_name(self):
        """
        Tests if we get correct results when user provides only the first name
        """

        transaction_data, size = get_transactions("Chris", "", "", "", "", "", 1, 100)

        assert size == 4
        for transaction in transaction_data:
            assert transaction["full_name"] == "Chris L. Anderson"


    def test_get_transactions_with_first_and_last_name_filtered(self):
        """
        Tests if we get correct results when user provides first and last name
        """

        transaction_data, size = get_transactions("Daven", "Thakkar", "", "", "", "", 1, 100)

        assert size == 8
        for transaction in transaction_data:
            assert transaction["full_name"] == "Daven C. Thakkar"


    def test_get_transactions_with_dates_filtered(self):
        """
        Tests if we get correct results when user provides the start and end dates
        """

        transaction_data, size = get_transactions(
            "", "", "", "",
            "2024/10/01",
            "2024/10/30",
            1,
            100
        )

        assert size == 12
        assert transaction_data is not None


    def test_get_transactions_with_end_date_filtered(self):
        """
        Tests if we get correct results when user provides only the end date
        """

        transaction_data, size = get_transactions("", "", "", "", "", "2024/10/30", 1, 100)

        assert size == 22
        assert transaction_data is not None


    def test_get_transactions_with_politician_type_filtered(self):
        """
        Tests if we get correct results when user provides the politician type
        """

        transaction_data, size = get_transactions("", "", "Senate", "", "", "", 1, 100)

        assert size == 12
        for transaction in transaction_data:
            assert transaction["politician_type"] == "Senate"


    def test_get_transactions_with_politician_hosue_filtered(self):
        """
        Tests if we get correct results when user provides the politician house
        """

        transaction_data, size = get_transactions("", "", "", "R", "", "", 1, 100)

        assert size == 6
        for transaction in transaction_data:
            assert transaction["politician_house"] == "R"


    def test_get_transactions_with_invalid_page_number_filtered(self):
        """
        Tests if we get correct results when user provides invalid page number
        """

        transaction_data, size = get_transactions("", "", "", "", "", "", 0, 100)

        assert size == 22
        assert transaction_data is not None


    def test_get_transactions_with_invalid_page_size_filtered(self):
        """
        Tests if we get correct results when user provides invalid page size
        """

        transaction_data, size = get_transactions("", "", "", "", "", "", 1, 101)

        assert size == 22
        assert transaction_data is not None
