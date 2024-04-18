from django.contrib import admin
from django.utils.html import format_html
from .models import CropType


class CropTypeAdmin(admin.ModelAdmin):
    list_display = ('croptype_name', 'slug', 'description', 'display_crop_image')
    readonly_fields = ('display_crop_image',)

    def display_crop_image(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.crop_image.url))

    display_crop_image.short_description = 'Crop Image Preview'

admin.site.register(CropType, CropTypeAdmin)
