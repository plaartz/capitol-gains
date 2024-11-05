from datetime import datetime, timedelta
from django.db.models import Exists, OuterRef, Q
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
        delta = (datetime.now().date() - date).days + 1
        if ticker not in stocks:
            stocks[ticker] = delta
        elif stocks[ticker] < delta:
            stocks[ticker] = delta


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

# pylint: disable=too-many-branches
def upload_stock_prices(data: dict) -> int:
    """
    Update stock price information in the database or add new entries to the database.
    
    :param data: dictionary of the stock prices we will use to update the database
    @return     Returns a status code depending on if uploading the stock prices was successful
    """
    try:
        items_to_update = []
        new_items = []
        existing_items = []
        for ticker, item_data in data.items():
            # Give an error if the stock price isn't a valid number
            for stock_price in item_data['prices']:
                if 'price' not in stock_price or 'date' not in stock_price:
                    continue
                if not isinstance(stock_price['price'], float):
                    try:
                        stock_price['price'] = float(stock_price['price'])
                    except ValueError:
                        continue
                if stock_price['price'] < 0:
                    continue
                price = stock_price['price']
                date = datetime.strptime(stock_price['date'], '%Y-%m-%d').date()

                # Don't create/update stock price if the stock doesn't exist
                stock_object = Stock.objects.filter(ticker=ticker).first()
                if stock_object is None:
                    continue

                item = StockPrice(stock=stock_object, price=price, date=date)
                items_to_update.append(item)
        existing_stock_prices = StockPrice.objects.filter(
            Q(stock__in=[item.stock for item in items_to_update]) &
            Q(date__in=[item.date for item in items_to_update])
        )
        # Map existing entries by (stock, date) for easier access
        existing_map = {
            (stock_price.stock, stock_price.date): stock_price
            for stock_price in existing_stock_prices
        }

        # Separate items to update (existing) from items to create (new)
        for item in items_to_update:
            if (item.stock, item.date) in existing_map:
                existing_map[(item.stock, item.date)].price = item.price
                existing_items.append(existing_map[(item.stock, item.date)])
            else:
                new_items.append(item)

        # Perform bulk_update on existing items and bulk_create on new items
        StockPrice.objects.bulk_update(existing_items, ['price'])
        StockPrice.objects.bulk_create(new_items)
        return 200
    except (KeyError, TypeError, ValueError):
        return 400
    except IntegrityError:
        return 409
    except (DatabaseError, ObjectDoesNotExist):
        return 500
    # pylint: disable=broad-except
    except Exception:
        return 500
