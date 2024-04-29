from django.shortcuts import render, redirect
from farm.models import Farm
from .models import Cart, CartItem
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required




def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Farm, id=product_id)

    if current_user.is_authenticated:
        try: 
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        
        cart.save()


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, 
                quantity=1, 
                user=current_user,
    )

            cart_item.save()

        return redirect('cart')
    
    else:
        try: 
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        
        cart.save()

        cart_item_qs = CartItem.objects.filter(product=product, cart=cart)

        if cart_item_qs.exists(): 
            cart_item = cart_item_qs.first()
            cart_item.quantity += 1
            cart_item.save()
        else: 
            cart_item = CartItem.objects.create(
                product=product, 
                quantity=1, 
                cart=cart,
            )
            cart_item.save()
    
        return redirect('cart')
    



def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Farm, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item does not exist

    return redirect('cart')




def remove_cart_item(request, product_id):

    product = get_object_or_404(Farm, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, cart=cart, user=request.user)
    else: 
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')

    


def cart(request, total=0, quantity=0, cart_items=None):
    try:

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items, 
    }

    return render(request, 'farm/cart.html', context)



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items, 
    }
    return render(request, 'farm/checkout.html', context)