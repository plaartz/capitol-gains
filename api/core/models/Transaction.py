# pylint: disable=too-few-public-methods
from django.db import models
from .Politician import Politician
from .Stock import Stock
from .StockPrice import StockPrice

class Transaction(models.Model):
    """
    Django model that represents a politician's transaction.
    """
    politician = models.ForeignKey(
        Politician,
        on_delete = models.CASCADE
    )
    stock = models.ForeignKey(
        Stock,
        on_delete = models.PROTECT
    )
    transaction_amount = models.CharField(max_length=50)
    transaction_date = models.DateField()
    disclosure_date = models.DateField()
    transaction_type = models.CharField(max_length=10)

    @property
    def percent_gain(self):
        """
        Represents a transaction's percent gain from the most recent purchase date.

        @return a float being 0.0 if the transaction is a purchase or an approximation of 
            the percent gain if it's a sale.
        """
        if self.transaction_type == "Purchase":
            return 0

        # Otherwise it's a sale.

        stock_prices = StockPrice.objects.filter(
            stock = self.stock
        )
        curr_price = stock_prices.filter(
            date = self.transaction_date
        ).first()

        if not curr_price:
            return 0
        curr_price = curr_price.price

        purchase_date = Transaction.objects.filter(
            politician = self.politician,
            stock = self.stock,
            transaction_type = "Purchase",
            transaction_date__lt = self.transaction_date
        ).values_list('transaction_date', flat=True).order_by('-transaction_date').first()

        old_price = stock_prices.filter(
            date = purchase_date
        ).first()

        if not old_price:
            return 0

        old_price = old_price.price
        return round((curr_price / old_price * 100) - 100, 2)
