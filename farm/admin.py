from django.contrib import admin
from .models import Farm

class FarmAdmin(admin.ModelAdmin):
    list_display = ['farm_name',  'stock', 'location', 'duration', 'price', 'custom_percentage', 'calculate_roi', 'total_roi_and_price', 'is_available']

    def total_roi_and_price(self, obj):
        return obj.calculate_roi() + obj.price
    total_roi_and_price.short_description = 'Total ROI and Price'

admin.site.register(Farm, FarmAdmin)
