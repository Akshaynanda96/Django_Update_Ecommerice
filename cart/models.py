from django.db import models
from base.models import BaseModole
from project.models import Product
from django.contrib.auth.models import User



class Carts(BaseModole):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey( Product, to_field='udid', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.qty * self.product.product_price
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    