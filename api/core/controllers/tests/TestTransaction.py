from datetime import datetime

from django.test import TestCase
from core.controllers import transaction
from core.models import Transaction, Profile, Politician, Stock

class TestTransactionController(TestCase):
    """
    Tests the functionality of the transaction report controller
    """

    def test_upload_transaction_reports_successfully(self):
        """
        Tests if valid scraped data gets uploaded to the database successfully
        """
        pass

    def test_fail_transaction_missing_field(self):
        """
        Tests if a report with a missing field gets uploaded or not
        """
        pass

    def test_duplicate_entry(self):
        """
        Tests if a duplciate stock, policitian, profile, and politician don't get uploaded
        """
        pass
