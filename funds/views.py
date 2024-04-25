from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct 
from farm.models import Farm
import datetime
import json

# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    print(body)
    #store trasnaction details 
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()


    #move cart to order table 

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id  # Assuming 'order' is defined elsewhere and has an 'id' attribute
        orderproduct.payment = payment  # Assuming 'payment' is defined elsewhere
        orderproduct.user_id = request.user.id  # Assuming 'request.user.id' is valid
        orderproduct.product_id = item.product_id 
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()  # Corrected typo from 'sace()' to 'save()'


        #reduce quantity 

        product = Farm.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()



    return render(request, 'funds/payments.html')


def place_order(request, total=0, quantity=0, ):
    current_user = request.user

    #if the fund count is less than or equal to 0, then redirect back to project page

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('farm')
    
    

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity


    
    if request.method == 'POST':
        form =  OrderForm(request.POST)
        if form.is_valid():
            #store all the required information insied fund table 
            data = Order()
            data.user = current_user
            data.bank_name = form.cleaned_data['bank_name']
            data.account_name = form.cleaned_data['account_name']
            data.account_number = form.cleaned_data['account_number']
            data.branch_name = form.cleaned_data['branch_name']
            data.paypal_account_name = form.cleaned_data['paypal_account_name']
            data.paypal_email = form.cleaned_data['paypal_email']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generate order number

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d") #20240205
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered = False, order_number=order_number)
            context = {
                'order': order, 
                'cart_items' : cart_items, 
                'total': total,
            }
            return render(request, 'funds/payments.html', context)
        
        else:
            return redirect('checkout')










