from datetime import datetime
from django.db.models import Exists, OuterRef

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
            return today - datetime.timedelta(days=days_to_subtract)
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

    for ticker in all_stocks_today:
        if ticker not in stocks:
            stocks[ticker] = 1

    return [{"ticker": key, "date_range": val} for (key, val) in stocks.items()], 200
