from django.db import models
from . import Stock

class StockPrice(models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete = models.CASCADE
    )
    price = models.FloatField()
    date = models.DateField()