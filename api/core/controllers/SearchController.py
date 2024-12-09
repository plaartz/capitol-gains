# pylint: disable=too-many-positional-arguments, too-many-arguments, line-too-long
from core.serializers import TransactionSerializer
from core.models import Transaction
from django.db.models.functions import Cast
from django.db.models import IntegerField, CharField, Func, F, Value, Case, When
from django.db.models.query import QuerySet
from django.db.models import Q # we will use this for full name stuff

def filter_by_price(transactions: QuerySet[Transaction], min_price: int, max_price: int) -> QuerySet[Transaction]:
    """
    The method is a helper function to filter out the transactions that do not fall within the min_price or max_price

    :param transactions: a query set of transactions before we filter
    :param min_price: the minimum price of the transactions we get
    :param max_price: the maximum price of the transactinos we get
    @return    returns a query set of the transactions 
    """
    filtered_transactions = transactions.annotate(
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
    return filtered_transactions

def get_transactions(
        full_name = None,
        stock_ticker = None,
        is_purchase = None,
        is_sale = None,
        min_price = None,
        max_price = None,
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
        "full_name": "full_name",
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

    size = 0
    start_index = page_size*page_no - page_size
    end_index = page_size*page_no

    # start filtering
    filter_criteria = Q()
    # full_name filtering
    if full_name is not None and " " in full_name:    # If there is a space then we extract first and last name
        split_name = full_name.split(" ")
        first_name = split_name[0]
        last_name = split_name[-1]
        filter_criteria &= (Q(politician__profile__first_name__icontains=first_name) |
                            Q(politician__profile__last_name__icontains=last_name))
    else:    # If full_name is None or there is just one word provided in the full_name
        if full_name: # if full_name is not None and there is only one word provided in full_name
            filter_criteria &= (Q(politician__profile__first_name__icontains=full_name) |
                                Q(politician__profile__last_name__icontains=full_name))

    # stock_ticker filtering
    if stock_ticker:
        filter_criteria &= Q(stock__ticker=stock_ticker)

    # transaction_type filtering
    if is_purchase and not is_sale:
        filter_criteria &= Q(transaction_type='Purchase')
    elif is_sale and not is_purchase:
        filter_criteria &= Q(transaction_type='Sale')

    # start_date and end_date filtering
    if start_date:
        filter_criteria &= Q(transaction_date__gte=start_date.replace("/", "-"))
    if end_date:
        filter_criteria &= Q(transaction_date__lte=end_date.replace("/", "-"))

    # Adjust needed ordering
    ordered_transactions = None    # Will hold the correctly ordered data

    if order_by not in set(["stock_price", "percent_gain", "full_name"]):
        # We order within transaction objects via ORM which is before the serializing
        ordering = valid_options[order_by]
        # Determines whether we need a negative for decending
        if order == "DESC":
            ordering = "-" + ordering

        # Get needed transactions
        transactions = filter_by_price(
                Transaction.objects.filter(filter_criteria),
                min_price,
                max_price
            ).order_by(ordering)

        # Serialize the transactions

        if no_gain and positive_gain:
            transactions = [ot for ot in transactions if ot.percent_gain >= 0]
        elif no_gain and negative_gain:
            transactions = [ot for ot in transactions if ot.percent_gain <= 0]
        elif positive_gain and negative_gain:
            transactions = [ot for ot in transactions if ot.percent_gain > 0 or ot.percent_gain < 0]
        elif no_gain:
            transactions = [ot for ot in transactions if ot.percent_gain == 0]
        elif positive_gain:
            transactions = [ot for ot in transactions if ot.percent_gain > 0]
        elif negative_gain:
            transactions = [ot for ot in transactions if ot.percent_gain < 0]

        size = len(transactions)
        transactions = transactions[start_index:end_index]
        ordered_transactions = TransactionSerializer(transactions, many = True).data
    else:
        # If we are ordering by "stock price" or "percent gain" or "full name" we will have to "order" after serializing
        is_reversed = False
        if order == "DESC":
            is_reversed = True

        # Get transactions
        transactions = filter_by_price(
            Transaction.objects.filter(filter_criteria),
            min_price,
            max_price
        )

        # Serialize the transactions
        transaction_data = TransactionSerializer(transactions, many = True).data

        # Order the data
        # pylint: disable=line-too-long
        ordered_transactions = sorted(transaction_data, key=lambda x: x[order_by], reverse = is_reversed)

        if no_gain and positive_gain:
            ordered_transactions = [ot for ot in ordered_transactions if ot['percent_gain'] >= 0]
        elif no_gain and negative_gain:
            ordered_transactions = [ot for ot in ordered_transactions if ot['percent_gain'] <= 0]
        elif positive_gain and negative_gain:
            ordered_transactions = [ot for ot in ordered_transactions if ot['percent_gain'] > 0 or ot['percent_gain'] < 0]
        elif no_gain:
            ordered_transactions = [ot for ot in ordered_transactions if ot['percent_gain'] == 0]
        elif positive_gain:
            ordered_transactions = [ot for ot in ordered_transactions if ot['percent_gain'] > 0]
        elif negative_gain:
            ordered_transactions = [ot for ot in ordered_transactions if ot['percent_gain'] < 0]

        size = len(ordered_transactions)
        ordered_transactions = ordered_transactions[start_index:end_index]
    return ordered_transactions, size
