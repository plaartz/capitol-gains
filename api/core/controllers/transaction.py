from datetime import datetime, date, timedelta
from django.db.utils import IntegrityError, DatabaseError
from core.models import Transaction, Stock, Profile, Politician, StockPrice

GRAPH_SIZE = 30

def process_profile(transaction: dict) -> Profile:
    """
    Process and get or create Profile from transaction data.
    """
    first_name = transaction['first_name']
    last_name = transaction['last_name']
    middle_initial = transaction['middle_initial']

    profile, _ = Profile.objects.get_or_create(
        first_name=first_name,
        middle_initial=middle_initial,
        last_name=last_name
    )
    return profile


def process_politician(profile: Profile, transaction: dict) -> Politician:
    """
    Process and get or create Politician from transaction data.
    """
    politician_type = transaction['filer_type']
    politician_house = 'I'

    politician, _ = Politician.objects.get_or_create(
        profile=profile,
        politician_type=politician_type,
        politician_house=politician_house
    )
    return politician


def process_stock(trade: dict, index: int) -> Stock:
    """
    Process and get or create Stock from trade data.
    """
    ticker = trade['ticker'][index]
    stock_name = trade['stock_name'][index]
    stock_description = "--"
    try:
        stock = Stock.objects.get(ticker=ticker)
    except Stock.DoesNotExist:
        stock = Stock.objects.create(
            ticker=ticker,
            name=stock_name,
            description_short=stock_description
        )

    return stock


def process_transaction(politician: Politician, stock: Stock,
                        trade: dict, disclosure_date: datetime) -> Transaction:
    """
    Process and create Transaction from trade data.
    """
    transaction_amount = trade['transaction_amount']
    transaction_date = datetime.strptime(trade['transaction_date'], '%Y-%m-%d')
    transaction_type = trade['transaction_type']

    transaction = Transaction.objects.create(
        politician=politician,
        stock=stock,
        transaction_amount=transaction_amount,
        transaction_date=transaction_date,
        disclosure_date=disclosure_date,
        transaction_type=transaction_type
    )
    return transaction


def upload_transactions(transactions: list) -> int:
    """
    Controller to upload transactions scraped from government website to database.

    @param transactions:    a list of transactions reports.
    @return:                status code representing if the upload was successful or not.
    """
    # pylint: disable=duplicate-code
    try:
        for transaction in transactions:
            profile = process_profile(transaction)
            politician = process_politician(profile, transaction)
            disclosure_date = datetime.strptime(transaction['date_received'], '%Y-%m-%d')

            for trade in transaction['transactions']:
                for index in range(len(trade['ticker'])):
                    stock = process_stock(trade, index)
                    process_transaction(politician, stock, trade, disclosure_date)
        return 200
    except (KeyError, TypeError, ValueError):
        return 400
    except IntegrityError:
        return 409
    except DatabaseError:
        return 500
    # pylint: disable=broad-except
    except Exception:
        return 500

def get_price_information(transaction_id) -> tuple[list, int]:
    """
    Returns a list of prices for the 10 days before to 10 days after.

    :param transaction_id: The id of the transaction we want price data for.
    :return tuple[list, int]: returns a tuple of a list of prices and the status
    """
    try:
        transaction = Transaction.objects.get(id=transaction_id)

        start_date = date.min
        end_date = date.max

        if transaction.transaction_type == "Sale":
            start_date = Transaction.objects.filter(
                politician = transaction.politician,
                stock = transaction.stock,
                transaction_type = "Purchase",
                transaction_date__lt = transaction.transaction_date
            ).order_by(
                '-transaction_date'
            ).values_list('transaction_date', flat=True).first()

            end_date = transaction.transaction_date
            if not start_date:
                start_date =  end_date

        else: #Is a Purchase
            start_date = transaction.transaction_date
            end_date = Transaction.objects.filter(
                politician = transaction.politician,
                stock = transaction.stock,
                transaction_type = "Sale",
                transaction_date__gt = transaction.transaction_date
            ).order_by(
                'transaction_date'
            ).values_list('transaction_date', flat=True).first()
            if not end_date:
                end_date = start_date

        time_span = (end_date - start_date).days

        if time_span <= GRAPH_SIZE:
            try:
                delta = timedelta(days=(GRAPH_SIZE - time_span) / 2)
                start_date -= delta
                end_date += delta
            #pylint: disable=broad-exception-caught
            except Exception:
                # pylint: disable=line-too-long
                print("Err, ", transaction.stock, transaction.transaction_date, transaction.transaction_type)

        prices = StockPrice.objects.filter(
            stock = transaction.stock,
            date__gte = start_date,
            date__lte = end_date
        ).all().values('date','price').order_by('date')

        return list(prices), 200


    except Transaction.DoesNotExist:
        return [], 400
