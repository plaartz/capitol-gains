from datetime import datetime, timedelta
from django.db.models import Exists, OuterRef
from django.db.utils import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist

from core.models import Transaction, Stock, StockPrice


def get_stocks_to_update() -> tuple[list, int]:
    """
    This method queries the database to find stocks that have a transaction without 
    a matching stock price. Utilizes a greedy heuristic to ensure if we have a earlier
    transaction, we will have all stock prices after that date.

    @return     returns a tuple with a list of needed stocks to update prices for.
    """
    def get_most_recent_weekday():
        today = datetime.now().date()
        if today.weekday() >= 5:  # Saturday (5) or Sunday (6)
            # Move back to Friday
            days_to_subtract = today.weekday() - 4
            return today - timedelta(days=days_to_subtract)
        return today

    # Query StockPrice based on stock and date
    matching_price = StockPrice.objects.filter(
        stock=OuterRef('stock'),
        date=OuterRef('transaction_date')
    )

    today_price = StockPrice.objects.filter(
        stock=OuterRef('id'),
        date=get_most_recent_weekday()
    )

    # Query Transactions that don't have an existing stock price based on matching_price
    unmatched = Transaction.objects.annotate(
        has_price=Exists(matching_price)
    ).filter(has_price=False).values_list('stock__ticker','transaction_date').all()

    stocks = {}

    for ticker, date in unmatched:
        delta = datetime.now().date() - date
        if ticker not in stocks:
            stocks[ticker] = delta.days
        elif stocks[ticker] < delta.days:
            stocks[ticker] = delta.days

    # Add in the ones we don't have a price for the most recent weekday
    all_stocks_today = (Stock.objects
        .annotate(has_price=Exists(today_price))
        .filter(has_price=False)
        .exclude(ticker__in=unmatched.values_list("stock__ticker",flat=True))
        .values_list('ticker',flat=True))

    today = datetime.now().date()
    for ticker in all_stocks_today:
        if ticker not in stocks:
            if today.weekday() >= 5:
                stocks[ticker] = datetime.now().date().weekday() - 3
            else:
                stocks[ticker] = 1

    return [{"ticker": key, "date_range": val} for (key, val) in stocks.items()], 200

def upload_stock_prices(data: dict) -> int:
    """
    Update stock price information in the database or add new entries to the database.
    
    :param data: dictionary of the stock prices we will use to update the database
    @return     Returns a status code depending on if uploading the stock prices was successful
    """
    try:
        items_to_update = []
        for ticker, item_data in data.items():
            if 'price' not in item_data['prices'] or 'date' not in item_data['prices']:
                continue
            # Give an error if the stock price isn't a valid number
            for stock_price in item_data['prices']:
                if not isinstance(stock_price['price'], float):
                    try:
                        item_data['prices']['price'] = float(item_data['prices']['price'])
                    except ValueError:
                        continue
                if stock_price['price'] < 0:
                    continue
                price = stock_price['price']
                date = stock_price['date']

                # Don't create/update stock price if the stock doesn't exist
                stock_object = Stock.objects.filter(ticker=ticker)
                if not stock_object.exists():
                    continue

                item = StockPrice(stock=stock_object, price=price, date=date)
                items_to_update.append(item)
        StockPrice.objects.bulk_create(
            items_to_update,
            update_conflicts=True,
            unique_fields=['stock', 'date'],
            update_fields=['price']
        )
        return 200
    except (KeyError, TypeError, ValueError):
        return 400
    except IntegrityError:
        return 409
    except (DatabaseError, ObjectDoesNotExist):
        return 500
