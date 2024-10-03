from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    description_short = models.CharField(max_length=100)