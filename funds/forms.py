from django import forms 
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta: 
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'bank_name', 'account_name', 'account_number', 'branch_name', 'paypal_account_name', 'paypal_email']
