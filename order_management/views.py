from product_management.models import Category, Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from order_management.models import Customer, Order, Item
import json


@csrf_exempt
@login_required(login_url='/login/')
def new_order(request):
    """This is the new order view with login required.
    This function will create customer, create order
    order with order item from post request data.
    This function will render order html page with product 
    list in context. 

    """

    if request.method == 'POST':
        data = json.loads(request.POST['cart'])
        customer, created = create_or_get_customer(data)
        order = Order.objects.create(customer=customer, total_amount=0)
        order.total_amount = create_order_item(data, order)
        order.save()  
        messages.success(request, f'The new order added successfully.')
        return redirect('/')
    else:
        context = get_product_list()
        return render(request, 'order_management/order.html', context)

def get_product_list():
    """Get product list

    Returns
    -------
    products_list: dictionary
        Dictionary with product list

    """

    data = []
    for product in Product.objects.all():
        data.append({
            'id': str(product.id),
            'name': product.name,
            'price': product.unit_price,
            'current_stock': product.current_stock
        })
    return {'products_list': data}

def create_or_get_customer(data):
    """Create or get customer. Customer will get by phone number only.
    If not found it will create new customer

    Parameters
    ----------
    data : dictionary
        This is customer info

    Returns
    -------
    customer: object
        New customer object

    created: bool
        If customer exists then return false else true

    """
    customer, created = Customer.objects.get_or_create(
            phone=data['customerPhone'],
            defaults={
                'name': data['customerName'],
                'phone': data['customerPhone'],
                'email': data['customerEmail'],
            }
        )
    return customer, created

def create_order_item(data, order):
    """Create order items

    Parameters
    ----------
    data : list
        This is cart item list

    order : dictionary
        This is order object

    Returns
    -------
    total_amount: int
        Total amount of order 

    """

    total_amount = 0
    for item in data['cart']:
        Item.objects.create(
            order=order,
            product_id=item['productId'],
            quantity=item['quantity']
        )
        update_product_quantity(item)
        total_amount += item['productPrice']

    return total_amount

def update_product_quantity(item):
    """Update product quantity

    Parameters
    ----------
    item : dictionary
        This is cart info for individual order item

    """
    product = Product.objects.get(id=item['productId'])
    if product.current_stock >= item['quantity']:
        product.current_stock -= item['quantity']
    else:
        product.current_stock = 0
    product.save()
