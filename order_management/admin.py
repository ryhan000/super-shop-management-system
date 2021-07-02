from django.contrib import admin
from .models import Customer, Order, Item


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')

admin.site.register(Customer, CustomerAdmin)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount')


admin.site.register(Order, OrderAdmin)



class ItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product','quantity')


admin.site.register(Item, ItemAdmin)
