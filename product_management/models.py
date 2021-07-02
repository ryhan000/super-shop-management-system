from django.db import models
import uuid


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(db_column='category_id', primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(db_column='name', max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'Category'


class Product(models.Model):
    id = models.UUIDField(db_column='product_id', primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('product_management.Category', db_column='category_id', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(db_column='name', max_length=50)
    code = models.CharField(db_column='code', max_length=50)
    unit_price = models.IntegerField(db_column='unit_price')
    current_stock = models.IntegerField(db_column='current_stock')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Products'
        db_table = 'Product'


