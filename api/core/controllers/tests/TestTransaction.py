# pylint: disable=invalid-name
from datetime import datetime
from core.models import Profile, Politician, Stock, Transaction
from core.controllers import transaction
from django.test import TestCase
from django.db.utils import IntegrityError

class TransactionUploadControllerTest(TestCase):
    """
    Tests functionality of the transaction report controller
    """
    def setUp(self):
        """
        Set up test data
        """
        self.existing_profile = Profile.objects.create(
            first_name='John', middle_initial='A', last_name='Doe'
        )
        self.existing_politician = Politician.objects.create(
            profile=self.existing_profile, politician_type='Senator'
        )
        self.existing_stock = Stock.objects.create(
            ticker='AAPL', name='Apple', description_short='Tech company'
        )

    def test_upload_transactions_success(self):
        """
        Test the successful upload of valid transactions
        """
        mock_transactions = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': datetime.strptime('2024-10-24', '%Y-%m-%d'),
                'transactions': [
                    {
                        'ticker': 'AAPL',
                        'stock_name': 'Apple',
                        'comment': 'Tech company',
                        'transaction_amount': '$1000-$5000',
                        'transaction_date': datetime.strptime('2024-10-01', '%Y-%m-%d'),
                        'transaction_type': 'Sale'
                    }
                ]
            }
        ]

        status_code = transaction.upload_transactions(mock_transactions)

        self.assertEqual(status_code, 200)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_upload_transactions_existing_data(self):
        """
        Test that no duplicates are created when data already exists
        """
        mock_transactions = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': datetime.strptime('2024-10-24', '%Y-%m-%d'),
                'transactions': [
                    {
                        'ticker': 'AAPL',
                        'stock_name': 'Apple',
                        'comment': 'Tech company',
                        'transaction_amount': '$1000-$5000',
                        'transaction_date': datetime.strptime('2024-10-01', '%Y-%m-%d'),
                        'transaction_type': 'Sale'
                    }
                ]
            }
        ]

        status_code = transaction.upload_transactions(mock_transactions)

        self.assertEqual(status_code, 200)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_upload_transactions_invalid_data(self):
        """
        Test handling of invalid transactions
        """
        mock_transactions = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': 'Invalid Date',
                'transactions': []
            }
        ]

        status_code = transaction.upload_transactions(mock_transactions)
        self.assertEqual(status_code, 400)

    def test_upload_transactions_integrity_error(self):
        """
        Test handling of an IntegrityError during the upload process
        """
        mock_transactions = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': datetime.strptime('2024-10-24', '%Y-%m-%d'),
                'transactions': [
                    {
                        'ticker': 'AAPL',
                        'stock_name': 'Apple',
                        'comment': 'Tech company',
                        'transaction_amount': '$1000-$5000',
                        'transaction_date': datetime.strptime('2024-10-01', '%Y-%m-%d'),
                        'transaction_type': 'Sale'
                    }
                ]
            }
        ]

        Transaction.objects.create(
            politician=self.existing_politician,
            stock=self.existing_stock,
            transaction_amount='$1000-$5000',
            transaction_date=datetime.strptime('2024-10-01', '%Y-%m-%d'),
            disclosure_date=datetime.strptime('2024-10-24', '%Y-%m-%d'),
            transaction_type='Sale'
        )

        with self.assertRaises(IntegrityError):
            transaction.upload_transactions(mock_transactions)
