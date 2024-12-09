# pylint: disable=duplicate-code, too-many-public-methods
import json
from datetime import datetime
from django.test import TestCase
from django.urls import reverse

class TestSearchView(TestCase):
    """
    Tests the functionality of our search view
    """

    fixtures = [
        "core/views/tests/fixtures/search.json"
    ]

    def make_post_request(self, body_query, query_string):
        """
        Helper method to make a POST request to the search endpoint.
        """
        url = f"{reverse('Search')}?{query_string}"

        if body_query is None:
            return self.client.post(url, data=b'', content_type="application/json")

        return self.client.post(
            url,
            data=json.dumps(body_query),
            content_type="application/json"
        )


    def test_search_view_with_first_name(self):
        """
        Tests if we get correct response when user provides
        only the first name part
        """

        body_query = {
            "full_name": "Daven",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "",
            "end_date": ""
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8
        for transaction in response_data["data"]:
            assert "Daven" in transaction["full_name"]


    def test_search_view_with_last_name(self):
        """
        Tests if we get correct response when user provides
        only the last name part
        """

        body_query = {
            "full_name": "Thakkar",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "",
            "end_date": ""
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8
        for transaction in response_data["data"]:
            assert transaction["full_name"] == "Daven C. Thakkar"


    def test_search_view_with_first_and_last_name(self):
        """
        Tests if we get correct response when user provides first and last name
        """

        body_query = {
            "full_name": "Daven C. Thakkar",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "",
            "end_date": ""
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8
        for transaction in response_data["data"]:
            assert transaction["full_name"] == "Daven C. Thakkar"


    def test_search_view_with_end_date(self):
        """
        Tests if we get correct response when user provides only the end date
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 10
        for transaction in response_data["data"]:
            end_date = datetime.strptime(body_query["end_date"], "%Y/%m/%d")
            transaction_date_correct_str = transaction["transaction_date"].replace("-", "/")
            transaction_date = datetime.strptime(transaction_date_correct_str, "%Y/%m/%d")
            assert transaction_date <= end_date


    def test_search_view_with_start_and_end_date(self):
        """
        Tests if we get correct response when user provides the start and end dates
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8
        for transaction in response_data["data"]:
            start_date = datetime.strptime(body_query["start_date"], "%Y/%m/%d")
            end_date = datetime.strptime(body_query["end_date"], "%Y/%m/%d")
            transaction_date_correct_str = transaction["transaction_date"].replace("-", "/")
            transaction_date = datetime.strptime(transaction_date_correct_str, "%Y/%m/%d")
            assert transaction_date >= start_date
            assert transaction_date <= end_date


    def test_search_view_with_invalid_page_number(self):
        """
        Tests if we get correct response when user provides invalid page number
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=0&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8


    def test_search_view_with_invalid_page_size(self):
        """
        Tests if we get correct response when user provides invalid page size
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=101"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8


    def test_search_view_with_no_page_size(self):
        """
        Tests if we get correct response when user provides no page size
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8


    def test_search_view_with_no_page_number(self):
        """
        Tests if we get correct response when user provides no page number
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8


    def test_search_view_with_no_page_number_and_no_page_size(self):
        """
        Tests if we get correct response when user provides no page number
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = ""

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8


    def test_search_view_with_no_body(self):
        """
        Tests if we get correct response when user provides no body
        """

        body_query = None
        query_string = ""

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 400
        assert response['Content-Type'] == 'application/json'
        response_data = json.loads(response.content)
        assert response_data["error"] == "No body provided!"


    def test_search_view_with_bad_page_number(self):
        """
        Tests if we get correct response when user provides no page number
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=test"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 400
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["error"] == "pageNo must be an integer!"

    def test_search_view_with_bad_page_size(self):
        """
        Tests if we get correct response when user provides no page number
        """

        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageSize=test"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 400
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["error"] == "pageSize must be an integer!"


    def test_search_view_with_order_by_transaction_date(self):
        """
        Tests if we get correct response when user provides transaction date for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=transaction_date"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by transaction date
        for i in range(0, len(transaction_data) - 1):
            current_date = transaction_data[i]["transaction_date"]
            next_date = transaction_data[i+1]["transaction_date"]
            current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            next_date_obj = datetime.strptime(next_date, "%Y-%m-%d")
            assert current_date_obj >= next_date_obj



    def test_search_view_with_order_by_disclosure_date(self):
        """
        Tests if we get correct response when user provides disclosure date for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=disclosure_date"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by disclosure date
        for i in range(0, len(transaction_data) - 1):
            current_date = transaction_data[i]["disclosure_date"]
            next_date = transaction_data[i+1]["disclosure_date"]
            current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            next_date_obj = datetime.strptime(next_date, "%Y-%m-%d")
            assert current_date_obj >= next_date_obj


    def test_search_view_with_order_by_transaction_type(self):
        """
        Tests if we get correct response when user provides transaction type for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=transaction_type"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by transaction type
        for i in range(0, len(transaction_data) - 1):
            current_type = transaction_data[i]["transaction_type"]
            next_type = transaction_data[i+1]["transaction_type"]
            assert current_type >= next_type


    def test_search_view_with_order_by_full_name(self):
        """
        Tests if we get correct response when user provides full name for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=full_name"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by first name
        for i in range(0, len(transaction_data) - 1):
            current_first_name = transaction_data[i]["full_name"].split(" ")[0]
            next_first_name = transaction_data[i+1]["full_name"].split(" ")[0]
            assert current_first_name >= next_first_name


    def test_search_view_with_order_by_last_name(self):
        """
        Tests if we get correct response when user provides last name for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=last_name"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by last name
        for i in range(0, len(transaction_data) - 1):
            current_last_name = transaction_data[i]["full_name"].split(" ")[-1]
            next_last_name = transaction_data[i+1]["full_name"].split(" ")[-1]
            assert current_last_name >= next_last_name


    def test_search_view_with_order_by_stock_ticker(self):
        """
        Tests if we get correct response when user provides stock ticker for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=stock_ticker"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by stock ticker
        for i in range(0, len(transaction_data) - 1):
            current_ticker = transaction_data[i]["stock_ticker"]
            next_ticker = transaction_data[i+1]["stock_ticker"]
            assert current_ticker >= next_ticker


    def test_search_view_with_order_by_stock_price(self):
        """
        Tests if we get correct response when user provides stock price for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=stock_price"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by stock price
        for i in range(0, len(transaction_data) - 1):
            current_price = float(transaction_data[i]["stock_price"])
            next_price = float(transaction_data[i+1]["stock_price"])
            assert current_price >= next_price


    def test_search_view_with_order_by_transaction_amount(self):
        """
        Tests if we get correct response when user provides transaction amount for ordering
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=transaction_amount"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by transaction amount
        for i in range(0, len(transaction_data) - 1):
            current_amount = int(transaction_data[i]["transaction_amount"])
            next_amount = int(transaction_data[i+1]["transaction_amount"])
            assert current_amount >= next_amount


    def test_search_view_with_order_ascending(self):
        """
        Tests if we get correct response when user provides first name
        for ordering and order ascending
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=full_name&order=ASC"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are ascending order by full name
        for i in range(0, len(transaction_data) - 1):
            current_full_name = transaction_data[i]["full_name"]
            next_full_name = transaction_data[i+1]["full_name"]
            assert current_full_name <= next_full_name


    def test_search_view_with_order_descending(self):
        """
        Tests if we get correct response when user provides full name
        for ordering and order descending
        """
        body_query = {
            "full_name": "",
            "stock_ticker": "",
            "is_purchase": False,
            "is_sale": False,
            "min_price": 0,
            "max_price": 1000000000,
            "positive_gain": False,
            "negative_gain": False,
            "no_gain": False,
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = "pageNo=1&pageSize=100&orderBy=full_name&order=DESC"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8

        transaction_data = response_data["data"]
        # Make sure all transactions are decending order by full name
        for i in range(0, len(transaction_data) - 1):
            current_full_name = transaction_data[i]["full_name"]
            next_full_name = transaction_data[i+1]["full_name"]
            assert current_full_name >= next_full_name
