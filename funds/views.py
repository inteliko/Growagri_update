from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order
import datetime
# Create your views here.

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
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['first_name']
            data.email = form.cleaned_data['email']     
            data.bank_name = form.cleaned_data['bank_name']
            data.account_name = form.cleaned_data['account_name']
            data.account_number = form.cleaned_data['account_number']
            data.branch_name = form.cleaned_data['branch_name']
            data.paypal_account_name = form.cleaned_data['paypal_account_name']
            data.paypal_email = form.cleaned_data['paypal_email']
            data.order_total = total
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
            return redirect('checkout')
        
        else:
            return redirect('checkout')










