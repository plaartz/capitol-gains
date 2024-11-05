from datetime import datetime
from django.db.utils import IntegrityError, DatabaseError
from core.models import Transaction, Stock, Profile, Politician

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

    stock, _ = Stock.objects.get_or_create(
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
