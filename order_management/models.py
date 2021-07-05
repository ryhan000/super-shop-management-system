from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import uuid
from datetime import date

today = date.today()


def generate_invoice_no():
    no = Order.objects.count()
    return no + 1


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
    qr_code = models.ImageField(db_column='QR_code', null=True, blank=True, upload_to='qrcode')
    invoice_no = models.IntegerField(db_column='invoice_no', default=generate_invoice_no)

    def __str__(self):
        return str(self.customer.name)

    def save(self, *args, **kwargs):
        # Ganarete QR Code image with customer and invoice information. After that save it.
        info = f"Date: {today} \n Invoice No:{generate_invoice_no()-1} \n Name: {self.customer.name}  \n Phone:  {self.customer.phone}  \n Email: {self.customer.email}"
        qr_code_image = qrcode.make(info)
        canvas = Image.new('RGB', (500, 500), 'white')
        ImageDraw.Draw(canvas)
        canvas.paste(qr_code_image)
        fname = f'qr_code-{self.id}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

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