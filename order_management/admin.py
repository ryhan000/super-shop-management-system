from django.contrib import admin
from django.shortcuts import HttpResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from order_management.models import Customer, Order, Item
from django.contrib import messages
from django.conf import settings
from datetime import date
from weasyprint import HTML
import inflect


def ganarate_pdf(template, content_disposition, data, total_in_word, total, customer_info):
    """Geneate invoice and download invoice as a PDF

    Parameters
    ----------
    template : html page name
        Like invoice.html

    content_disposition : string
        'attachment; filename="Invoice.pdf"'

    data : list
        This is the list of order item

    total_in_word : string
        Like fifty

    total : int
        Total order amount

    customer_info : file
        This is the QR code with customer and invoice information.

    Returns
    -------
    HttpResponse
    """

    context = {
        'page_size': 'A4', 
        'queryset': data, 
        'total_in_word': total_in_word, 
        'total': total,
        'customer_info': customer_info,
    }

    html_string = render_to_string(template, context=context)
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/invoice.pdf')

    fs = FileSystemStorage('/tmp')
    with fs.open('invoice.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = content_disposition
        return response
    return response

def get_order_items(order):
    """Get order items list

    Parameters
    ----------
    order : object
        This is the order object

    Returns
    -------
    total_amount: int
        total order amount 

    data: list
        Order item list

    """

    data = []
    index = 1
    total_amount = 0

    for item in order.items.all():
        single_item = {}
        item_total = item.quantity * item.product.unit_price
        single_item['index'] = index
        single_item['product_name'] = item.product.name
        single_item['unit_price'] = item.product.unit_price
        single_item['quantity'] = item.quantity
        single_item['item_total'] = item_total
        data.append(single_item)
        total_amount += item_total
        index += 1

    return total_amount, data


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    list_filter = ('created_at', )

admin.site.register(Customer, CustomerAdmin)


class ItemAdmin(admin.TabularInline):
    model = Item
    fieldsets = (
        ('Item Info', {'fields': ('order', 'product','quantity')}),
    )
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemAdmin, ]
    list_display = ('customer', 'total_amount', 'created_at')
    exclude = ['qr_code', ]
    list_filter = ('created_at', )
    actions = ['generate_invoice']

    def generate_invoice(modeladmin, request, queryset):
        """Geneate invoice and download invoice as a PDF

        Parameters
        ----------
        queryset : order list
            This is the list of selected order

        Returns
        -------
        HttpResponse

        """

        if queryset.count() > 1:
            messages.warning(request, ' Please, select one order at a time for invoice generate.')
            return None

        order = queryset.first()
        template = "invoice.html"
        content_disposition = 'attachment; filename="Invoice.pdf"'
        total_amount, order_items = get_order_items(order)
        total_in_word = inflect.engine().number_to_words(total_amount)
        customer_info = f'{settings.TLD}{order.qr_code.url}'
        return ganarate_pdf(template, content_disposition, order_items, total_in_word.title(), total_amount, customer_info)

    generate_invoice.short_description = 'Generate invoice'


admin.site.register(Order, OrderAdmin)
