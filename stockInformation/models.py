from __future__ import unicode_literals

from django.db import models


class Stocks(models.Model):
    symbol = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    change = models.CharField(max_length=200)

    def __str__(self):
        return self.symbol, self.name, self.price, self.change
