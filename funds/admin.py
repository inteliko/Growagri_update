from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'payment', 'status', 'is_ordered', 'created_at', 'updated_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'user__username', 'payment__payment_id']  # Assuming Account model has a 'username' field
    list_per_page = 20

    inlines = [OrderProductInline]




admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
