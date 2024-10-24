# pylint: disable=duplicate-code
import json
from datetime import datetime
from django.test import TestCase
from django.urls import reverse

class TestSearchView(TestCase):
    """
    Tests the functionality of our search view
    """

    fixtures = [
        "api/fixtures/StockFixture.json", 
        "api/fixtures/StockPriceFixture.json", 
        "api/fixtures/ProfileFixture.json", 
        "api/fixtures/PoliticianFixture.json", 
        "api/fixtures/TransactionFixture.json"
    ]

    def make_post_request(self, body_query, query_string):
        """
        Helper method to make a POST request to the search endpoint.
        """
        url = f"{reverse('search')}?{query_string}"
        return self.client.post(
            url,
            data=json.dumps(body_query),
            content_type="application/json"
        )


    def test_search_view_with_first_name(self):
        """
        Tests if we get correct response when user provides first name
        """

        body_query = {
            "first_name": "Daven",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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


    def test_search_view_with_last_name(self):
        """
        Tests if we get correct response when user provides last name
        """

        body_query = {
            "first_name": "",
            "last_name": "Thakkar",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "Chris",
            "last_name": "Anderson",
            "politician_type": "",
            "politician_house": "",
            "start_date": "",
            "end_date": ""
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 4
        for transaction in response_data["data"]:
            assert transaction["full_name"] == "Chris L. Anderson"


    def test_search_view_with_politician_type(self):
        """
        Tests if we get correct response when user provides the politician type
        """

        body_query = {
            "first_name": "",
            "last_name": "",
            "politician_type": "Senate",
            "politician_house": "",
            "start_date": "",
            "end_date": ""
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 12
        for transaction in response_data["data"]:
            assert transaction["politician_type"] == "Senate"


    def test_search_view_with_politician_house(self):
        """
        Tests if we get correct response when user provides the politician house
        """

        body_query = {
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "R",
            "start_date": "",
            "end_date": ""
        }
        query_string = "pageNo=1&pageSize=100"

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 6
        for transaction in response_data["data"]:
            assert transaction["politician_house"] == "R"


    def test_search_view_with_end_date(self):
        """
        Tests if we get correct response when user provides only the end date
        """

        body_query = {
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
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
            "first_name": "",
            "last_name": "",
            "politician_type": "",
            "politician_house": "",
            "start_date": "2024/09/01",
            "end_date": "2024/09/30"
        }
        query_string = ""

        response = self.make_post_request(body_query, query_string)

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'

        response_data = json.loads(response.content)
        assert response_data["size"] == 8
