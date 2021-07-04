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


def get_pdf(template, content_disposition, data, total_in_word, total, customer_info):

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


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')

admin.site.register(Customer, CustomerAdmin)


class ItemAdmin(admin.TabularInline):
    model = Item
    fieldsets = (
        ('Item Info', {'fields': ('order', 'product','quantity')}),
    )
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemAdmin, ]
    list_display = ('customer', 'total_amount')
    actions = ['generate_invoice']

    def generate_invoice(modeladmin, request, queryset):

        if queryset.count() > 1:
            messages.warning(request, ' Please, select one order at a time for invoice generate.')
            return None

        order = queryset.first()
        template = "invoice.html"
        content_disposition = 'attachment; filename="Invoice.pdf"'

        data = []
        index = 1
        total = 0

        for item in order.items.all():
            single_item = {}
            item_total = item.quantity * item.product.unit_price
            single_item['index'] = index
            single_item['product_name'] = item.product.name
            single_item['unit_price'] = item.product.unit_price
            single_item['quantity'] = item.quantity
            single_item['item_total'] = item_total
            data.append(single_item)
            total += item_total
            index += 1

        total_in_word = inflect.engine().number_to_words(total)
        customer_info = f'{settings.TLD}{order.qr_code.url}'
        return get_pdf(template, content_disposition, data, str(total_in_word).title(), total, customer_info)

    generate_invoice.short_description = 'Generate invoice'


admin.site.register(Order, OrderAdmin)
