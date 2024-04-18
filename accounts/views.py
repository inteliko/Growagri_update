from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth.decorators import login_required




# Create your views here.

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
            messages.success(request, 'Registration Successful')
            return redirect('register')

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

        user = authenticate(request, email=email, password=password)  # Using authenticate instead of auth.authenticate

        if user is not None:
            auth_login(request, user)  # Using auth_login instead of login
            messages.success(request, 'You are logged in.')
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
    return render(request, 'dashboard/dashboard.html')


