import re
from tabnanny import verbose
from django import db
from django.db import models
from goods.models import Product
from users.models import User


class CartQuerySet(models.QuerySet):
    
    def total_price(self):
        return round(sum([cart.products_price() for cart in self.all()]), 2)
    
    def total_quantity(self):
        if self:
            return sum([cart.quantity for cart in self.all()])
    
        return 0

        
class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Користувачі")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")
    session_key = models.CharField(max_length=32, null=True, blank=True, verbose_name="Ключ сесії")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    
    objects = CartQuerySet.as_manager()
    class Meta:
        db_table = "carts"
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"
        
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)
        
    def __str__(self):
        return f'Кошик {self.user.username} | Товар {self.product.name} | Кількість {self.quantity}'