from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from funds.models import Order


#Email Verification 

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests


#views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split("@")[0]

            user = Account.objects.create_user(first_name = first_name, last_name=last_name,username=username, email=email, password=password )
            user.phone_number = phone_number
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user, 
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'Registration Successful')
            return redirect('/accounts/login/?command=verification&email='+email)

    else: 
            form = RegistrationForm

    context = {
        'form': form,
    }


    
  
    return render(request, 'accounts/register.html', context)





def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate( email=email, password=password)  # Using authenticate instead of auth.authenticate

        if user is not None:
          
            try:
               cart = Cart.objects.get(cart_id=_cart_id(request))
               is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
               
               if is_cart_item_exists:
                   cart_item = CartItem.objects.filter(cart=cart)

                   for item in cart_item:
                       item.user = user 
                       item.save()



            except:
             pass

            auth_login(request, user)  # Using auth_login instead of login
            messages.success(request, 'You are succesfully logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next>/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
               
            except:
                 return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'accounts/login.html',{'user': request.user})



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')
    




def dashboard(request):
    orders = Order.objects.filter(user_id=request.user.id, is_ordered=True).order_by('created_at')
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'ordered_count': orders_count,
        'userprofile': userprofile,
    }

    return render(request, 'dashboard/dashboard.html', context)



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your Account is activate')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
        
    
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save user data
            profile = profile_form.save(commit=False)  # Don't save yet, to set userprofile manually
            profile.user = request.user  # Set userprofile manually
            profile.save()  # Save userprofile
            messages.success(request, 'Your Profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Use get() method to safely get POST data

        if Account.objects.filter(email=email).exists():  # Corrected method name
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user, 
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def resetPassword_validate(request):
    return HttpResponse('ok')

def my_funds(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    order_products = []

    for order in orders:
        order_products.extend(order.orderproduct_set.all())

    context = {
        'orders': orders,
        'order_products': order_products,
    }

    return render(request, 'dashboard/my_funds.html', context)


