from django.db import models
import uuid


# Create your models here.
class Customer(models.Model):
    id = models.UUIDField(db_column='customer_id', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(db_column='name', max_length=50)
    phone = models.CharField(db_column='phone', max_length=50, unique=True)
    email = models.CharField(db_column='email', max_length=50)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Customers'
        db_table = 'Customers'


class Order(models.Model):
    id = models.UUIDField(db_column='order_id', primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('order_management.Customer', db_column='customer_id', on_delete=models.CASCADE, related_name='orders')
    total_amount = models.IntegerField(db_column='total_amount')
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)

    def __str__(self):
        return str(self.customer.name)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Orders'
        db_table = 'Order'


class Item(models.Model):
    id = models.UUIDField(db_column='item_id', primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('order_management.Order', db_column='order_id', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product_management.Product', db_column='product_id', on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(db_column='quantity')


    def __str__(self):
        return str(self.product.name)

    class Meta:
        verbose_name_plural = 'items'
        db_table = 'Item'