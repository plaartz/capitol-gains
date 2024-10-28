import json
from django.test import TestCase
from django.urls import reverse

class UploadTransactionInformationViewTest(TestCase):
    """
    Tests functionality of the transaction view
    """
    def make_post_request(self, transactions):
        """
        Helper method to make POST requets to transaction endpoint
        """
        return self.client.post(
            reverse("transaction"),
            data=json.dumps(transactions),
            content_type="application/json"
        )

    def test_successful_upload(self):
        data = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': '2024-01-10',
                'transactions': [
                    {
                        'transaction_number': 1,
                        'ticker': ['AAPL'],
                        'owner': 'John Doe',
                        'stock_name': ['Apple Inc.'],
                        'transaction_date': '2024-01-01',
                        'transaction_type': 'Purchase',
                        'transaction_amount': '$100 - $200',
                        'comment': 'Bought for portfolio',
                    }
                ]
            }
        ]

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "ok", "message": "Transactions uploaded"}
        )

    def test_invalid_json(self):
        response = self.make_post_request("invalid json")

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Invalid JSON"})

    def test_bad_request(self):
        data = [
            {
                'transactions': [
                    {
                        'transaction_number': 1,
                        'ticker': ['AAPL'],
                        'owner': 'John Doe',
                        'stock_name': ['Apple Inc.'],
                        'transaction_date': '2024-01-01',
                        'transaction_type': 'Purchase',
                        'transaction_amount': '$100 - $200',
                        'comment': 'Bought for portfolio',
                    }
                ]
            }
        ]

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Bad request, missing or invalid data"})

    def test_conflict_error(self):
        data = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': '2024-01-10',
                'transactions': [
                    {
                        'transaction_number': 1,
                        'ticker': ['AAPL'],
                        'owner': 'John Doe',
                        'stock_name': ['Apple Inc.'],
                        'transaction_date': '2024-01-01',
                        'transaction_type': 'Purchase',
                        'transaction_amount': '$100 - $200',
                        'comment': 'Bought for portfolio',
                    }
                ]
            }
        ]

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(response.content, {"error": "Conflict, integrity error with the database"})

    def test_internal_server_error(self):
        data = [
            {
                'first_name': 'John',
                'middle_initial': 'A',
                'last_name': 'Doe',
                'filer_type': 'Senator',
                'date_received': '2024-01-10',
                'transactions': [
                    {
                        'transaction_number': 1,
                        'ticker': ['AAPL'],
                        'owner': 'John Doe',
                        'stock_name': ['Apple Inc.'],
                        'transaction_date': '2024-01-01',
                        'transaction_type': 'Purchase',
                        'transaction_amount': '$100 - $200',
                        'comment': 'Bought for portfolio',
                    }
                ]
            }
        ]

        response = self.make_post_request(data)

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {"error": "Internal server error when uploading transactions"})
