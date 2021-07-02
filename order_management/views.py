from django.shortcuts import render
from product_management.models import Category, Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
@login_required(login_url='/admin/login/')
def new_order(request):

    if request.method == 'POST':
        # with transaction.atomic():
        #     data = json.loads(request.POST['cart'])

        #     is_pending = True if data['selectedStatus'] == 'Pending' else False

        #     remarks = data['remarks']
        #     customers = Customer.objects.filter(contact_number1=data['buyerContactNumber'])

        #     if not customers.exists():
        #         customer = Customer.objects.create(
        #             name=data['buyerName'],
        #             address=data['buyerAddress'],
        #             contact_number1=data['buyerContactNumber'],
        #             type=data['selectedCustomerType'],
        #         )
        #     else:
        #         customer = customers.first()
        #         customer.name = data['buyerName']
        #         customer.address = data['buyerAddress']
        #         customer.contact_number1 = data['buyerContactNumber']
        #         customer.type = data['selectedCustomerType']
        #         customer.save()

        #     order = Order.objects.create(customer=customer, total_amount=0, total_item_count=0, remarks=remarks, is_pending=is_pending)

        #     for item in data['cart']:
        #         product_batch = ProductBatch.objects.get(id=item['batchId'])
        #         for i in range(item['quantity']):
        #             OrderItem.objects.create(
        #                 order=order,
        #                 product_batch=product_batch,
        #                 quantity=1,
        #                 unit_price=int(item['productPrice'] / item['quantity'])
        #             )
        messages.success(request, f'The new order for {customer.name} was added successfully.')

        return redirect('..')
    else:
        products = Product.objects.all()
        context = {
            'products_list': [{'id': str(item.id), 'name': item.name, 'price': item.unit_price} for item in products]
        }
        return render(request, 'order_management/order.html', context)