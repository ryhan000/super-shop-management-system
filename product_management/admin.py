from django.contrib import admin
from product_management.models import Category, Product

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'unit_price', 'current_stock')


admin.site.register(Product, ProductAdmin)
