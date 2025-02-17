from django.db import models

from users.models import User
from goods.models import Product

# Create your models here.
class OrderItemQuerySet(models.QuerySet):

    def total_quantity(self):
        if self:
            return sum(item.quantity for item in self)
        return 0
    
    def total_price(self):
        return sum(item.product_price * item.quantity for item in self)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефону')
    requires_delivery = models.BooleanField(default=False, verbose_name='Потрібна доставка')
    delivery_address = models.CharField(null=True, blank=True, verbose_name='Адреса доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при отриманні')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=100, verbose_name='Статус замовлення')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Замовлення {self.id} | Покупець: {self.user.first_name} {self.user.last_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name = 'Замовлення')
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, default=None, verbose_name='Товар')
    name = models.CharField(max_length=255, verbose_name='Назва товару')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кількість')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Товар в замовленні'
        verbose_name_plural = 'Товари в замовленні'

    objects = OrderItemQuerySet.as_manager()

    def product_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f'Товар: {self.name} | Замовлення №: {self.order.id}'







