# pylint: disable=too-many-positional-arguments, too-many-arguments, line-too-long
from core.serializers import TransactionSerializer
from core.models import Transaction

def get_transactions(first_name, last_name, politician_type, politician_house, start_date, end_date, page_no, page_size):
    """
    The method gets all the transaction based on what filteration the user provides.

    @return    returns a list of the transactions 
    """

    # Handle page number
    if page_no is None:
        page_no = 1    # We are defaulting to the first page
    else:
        page_no = max(1, page_no)

    # Handle invalid page size
    if page_size is None:
        page_size = 100    # We are defaulting to page size 100
    else:
        page_size = min(max(page_size, 1), 100)    # Ensures 1 <= page size <= 100

    filter_criteria = {}
    if first_name:
        filter_criteria['politician__profile__first_name'] = first_name
    if last_name:
        filter_criteria['politician__profile__last_name'] = last_name
    if politician_type:
        filter_criteria['politician__politician_type'] = politician_type
    if politician_house:
        filter_criteria['politician__politician_house'] = politician_house
    if start_date:
        filter_criteria['transaction_date__gte'] = start_date.replace("/", "-")
    if end_date:
        filter_criteria['transaction_date__lte'] = end_date.replace("/", "-")

    # Get transactions
    transactions = Transaction.objects.filter(**filter_criteria)

    # Serialize the transactions
    transaction_data = TransactionSerializer(transactions, many = True).data

    # Return the correct number of transactions
    start_index = page_size*page_no - page_size
    end_index = page_size*page_no
    return transaction_data[start_index:end_index], len(transaction_data)
