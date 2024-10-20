# pylint: disable=too-few-public-methods
from django.db import models
from .Stock import Stock

class StockPrice(models.Model):
    """
    Django model that represents a stock's price at a certain date.
    """
    stock = models.ForeignKey(
        Stock,
        on_delete = models.CASCADE
    )
    price = models.FloatField()
    date = models.DateField()
