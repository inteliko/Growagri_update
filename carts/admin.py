from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'cart', 'quantity', 'is_active']
    list_filter = ['is_active']




admin.site.register( CartItem, CartItemAdmin)
