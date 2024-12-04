# pylint: disable=too-many-positional-arguments, too-many-arguments, line-too-long
from core.serializers import TransactionSerializer
from core.models import Transaction
from django.db.models.functions import Cast
from django.db.models import IntegerField, CharField, Func, F, Value, Case, When, Q
from django.db.models.query import QuerySet

def filter_by_price(transactions: QuerySet[Transaction], min_price: int, max_price: int) -> QuerySet[Transaction]:
    """
    The method is a helper function to filter out the transactions that do not fall within the min_price or max_price

    :param transactions: a query set of transactions before we filter
    :param min_price: the minimum price of the transactions we get
    :param max_price: the maximum price of the transactinos we get
    @return    returns a query set of the transactions 
    """
    filetered_transactions = transactions.annotate(
        # Find the position of the first " - " to split the string
        first_amount_pos=Func(
            F('transaction_amount'),
            Value(' - '),
            function='INSTR',
            output_field=IntegerField()
        ),
        # Extract the substring before the first " - ", handling case where there's no dash
        extracted_amount=Case(
            When(first_amount_pos=0, then=F('transaction_amount')),  # If no dash, use the whole string
            default=Func(
                F('transaction_amount'),
                1,
                F('first_amount_pos') - 1,
                function='SUBSTR',
                output_field=CharField()
            )
        ),
        # Clean up the amount by removing "$" and "," in one step and cast to integer
        clean_amount=Func(
            Func(
                F('extracted_amount'),
                Value('$'),
                Value(''),
                function='REPLACE',
                output_field=CharField()
            ),
            Value(','),
            Value(''),
            function='REPLACE',
            output_field=CharField()  # Result after second REPLACE
        ),
        extracted_transaction_amount=Cast(
            F('clean_amount'),
            output_field=IntegerField()  # Convert cleaned string to integer
        )
    ).filter(
        extracted_transaction_amount__gte=min_price,
        extracted_transaction_amount__lte=max_price
    )
    return filetered_transactions

def get_transactions(
        first_name = None,
        last_name = None,
        stock_ticker = None,
        is_purchase = None,
        is_sale = None,
        min_price = 0,
        max_price = 1000000000,
        positive_gain = None,
        negative_gain = None,
        no_gain = None,
        start_date = None,
        end_date = None,
        page_no = None,
        page_size = None,
        order_by = None,
        order = None,
        transaction_id=None):
    """
    The method gets all the transaction based on what filteration the user provides.

    @return    returns a list of the transactions 
    """

    # Make sure the order by is a valid selection
    valid_options = {
        "transaction_date": "transaction_date",
        "disclosure_date": "disclosure_date",
        "transaction_type": "transaction_type",
        "transaction_amount": "extracted_transaction_amount", # This is the holder used for ordering and casting
        "first_name": "politician__profile__first_name",
        "last_name": "politician__profile__last_name",
        "stock_ticker": "stock__ticker",
        "stock_price": "",
        "percent_gain":""
    }
    if order_by is None or order_by == "" or order_by.lower() not in valid_options:
        order_by = "transaction_date"
    order_by = order_by.lower()

    # Handle order
    if order is None or order == "" or (order.upper() not in ["ASC", "DESC"]):
        order = "DESC"
    order = order.upper()

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

    if transaction_id:
        transaction = Transaction.objects.get(id=transaction_id)
        if not transaction:
            return [], 0
        return TransactionSerializer([transaction],many=True).data, 1


    filter_criteria = {}
    if first_name:
        filter_criteria['politician__profile__first_name'] = first_name
    if last_name:
        filter_criteria['politician__profile__last_name'] = last_name
    if stock_ticker:
        filter_criteria['stock__ticker'] = stock_ticker
    if is_purchase and not is_sale:
        filter_criteria['transaction_type'] = 'Purchase'
    elif is_sale and not is_purchase:
        filter_criteria['transaction_type'] = 'Sale'

    gain_conditions = Q()
    if no_gain:
        gain_conditions |= Q(percent_gain=0)
    if positive_gain:
        gain_conditions |= Q(percent_gain__gt=0)
    if negative_gain:
        gain_conditions |= Q(percent_gain__lt=0)

    if start_date:
        filter_criteria['transaction_date__gte'] = start_date.replace("/", "-")
    if end_date:
        filter_criteria['transaction_date__lte'] = end_date.replace("/", "-")
    # Adjust needed ordering
    ordered_transactions = None    # Will hold the correctly ordered data

    if order_by not in  ["stock_price", "percent_gain"]:
        # We order within transaction objects via ORM which is before the serializing
        ordering = valid_options[order_by]
        # Determines whether we need a negative for decending
        if order == "DESC":
            ordering = "-" + ordering

        transactions = None    # Holds initial transaction query set
        # Order by "transaction amount" needs to be first parsed and casted to an integer
        if order_by == "transaction_amount":
            # Get transactions alongside parsing and casting via ORM

            transactions = filter_by_price(
                Transaction.objects.filter(gain_conditions).filter(**filter_criteria),
                min_price,
                max_price
            ).order_by(ordering)

        else:
            # Get transactions normally

            transactions = filter_by_price(
                Transaction.objects.filter(gain_conditions).filter(**filter_criteria),
                min_price,
                max_price
            ).order_by(ordering)

        # Serialize the transactions

        ordered_transactions = TransactionSerializer(transactions, many = True).data
    else:
        # If we are ordering by "stock price" or "percent gain" we will have to "order" after serializing
        is_reversed = False
        if order == "DESC":
            is_reversed = True

        # Get transactions
        transactions = filter_by_price(
            Transaction.objects.filter(gain_conditions).filter(**filter_criteria),
            min_price,
            max_price
        )

        # Serialize the transactions
        transaction_data = TransactionSerializer(transactions, many = True).data

        # Order the data
        ordered_transactions = sorted(transaction_data, key=lambda x: x[order_by], reverse = is_reversed)

    # Return the correct number of transactions
    start_index = page_size*page_no - page_size
    end_index = page_size*page_no
    sliced = ordered_transactions[start_index:end_index]

    return sliced, len(ordered_transactions)
