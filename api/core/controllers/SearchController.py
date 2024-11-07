# pylint: disable=too-many-positional-arguments, too-many-arguments, line-too-long, too-many-locals, too-many-branches, consider-iterating-dictionary, too-many-statements
from core.serializers import TransactionSerializer
from core.models import Transaction
from django.db.models.functions import Cast
from django.db.models import IntegerField, CharField, Func, F, Value, Case, When

def get_transactions(first_name, last_name, politician_type, politician_house, start_date, end_date, page_no, page_size, order_by, order):
    """
    The method gets all the transaction based on what filteration the user provides.

    @return    returns a list of the transactions 
    """

    # Make sure the order by is a valid selection
    valid_options = {
        "transaction_date": "transaction_date",
        "disclosure_date": "disclosure_date",
        "transaction_type": "transaction_type",
        "transaction_amount": "extracted_transaction_amount", # This is the holder used for ordering and casting (line 66 and 85)
        "politician_type": "politician__politician_type",
        "politician_house": "politician__politician_house",
        "first_name": "politician__profile__first_name",
        "last_name": "politician__profile__last_name",
        "stock_ticker": "stock__ticker",
        "stock_price": ""
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

    # Adjust needed ordering
    ordered_transactions = None    # Will hold the correctly ordered data
    if order_by != "stock_price":
        # We order within transaction objects via ORM which is before the serializing
        ordering = valid_options[order_by]
        # Determines whether we need a negative
        if order == "DESC":
            ordering = "-" + ordering

        transactions = None    # Holds initial transaction query set
        # Order by "transaction amount" needs to be first casted to an integer
        if order_by == "transaction_amount":
            # Get transactions with casting
            # This works for MySQL db, now seeing if it works for sqlite via pipeline
            transactions = Transaction.objects.filter(**filter_criteria).annotate(
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
                        F('first_amount_pos'),
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
            ).order_by(ordering)




            ''' The below uses SUBSTRING_INDEX which is only for MySQL db's
            # Extract and clean the first number before the dash
            transactions = Transaction.objects.filter(**filter_criteria).annotate(
                # Extract substring up to the first " - " (splits the string at the dash)
                first_amount=Func(
                    F('transaction_amount'),
                    Value(' - '),
                    Value(1),
                    function='SUBSTRING_INDEX',
                    output_field=CharField()  # Explicitly declare the output as CharField
                ),
                # Remove any "$" or "," from the extracted amount and convert to integer
                extracted_transaction_amount=Cast(
                    Func(
                        Func(F('first_amount'), Value('$'), Value(''), function='REPLACE'),
                        Value(','),
                        Value(''),
                        function='REPLACE',
                        output_field=CharField()  # Explicitly declare the output as CharField
                    ),
                    output_field=IntegerField()   # Explicityly declare final output as integer
                )
            ).order_by(ordering)'''
        else:
            # Get transactions normally
            transactions = Transaction.objects.filter(**filter_criteria).order_by(ordering)

        # Serialize the transactions
        ordered_transactions = TransactionSerializer(transactions, many = True).data
    else:
        # If we are ordering by "stock price" we will have to "order" after serializing
        is_reversed = False
        if order == "DESC":
            is_reversed = True

        # Get transactions
        transactions = Transaction.objects.filter(**filter_criteria)

        # Serialize the transactions
        transaction_data = TransactionSerializer(transactions, many = True).data

        # Order the data
        ordered_transactions = sorted(transaction_data, key=lambda x: x['stock_price'], reverse = is_reversed)

    # Return the correct number of transactions
    start_index = page_size*page_no - page_size
    end_index = page_size*page_no
    return ordered_transactions[start_index:end_index], len(ordered_transactions)
