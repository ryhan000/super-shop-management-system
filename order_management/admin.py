from django.contrib import admin
from order_management.models import Customer, Order, Item


# Register your models here.
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
    

admin.site.register(Order, OrderAdmin)


# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product','quantity')


# admin.site.register(Item, ItemAdmin)
