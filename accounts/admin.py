from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined') 
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;">'.format(obj.profile_picture.url))
        else:
            return "No Image"

    def nid_picture_thumbnail(self, obj):
        if obj.nid_picture:
            return format_html('<img src="{}" width="50">'.format(obj.nid_picture.url))
        else:
            return "No Image"

    def nomine_nid_picture_thumbnail(self, obj):
        if obj.nomine_nid_picture:
            return format_html('<img src="{}" width="50">'.format(obj.nomine_nid_picture.url))
        else:
            return "No Image"

    profile_picture_thumbnail.short_description = 'Profile Picture'
    nid_picture_thumbnail.short_description = 'NID Picture'
    nomine_nid_picture_thumbnail.short_description = 'Nomine NID Picture'

    list_display = ('user', 'dob', 'nid_number', 'profile_picture_thumbnail', 'nid_picture_thumbnail', 'nomine_name', 'nomine_nid_number', 'nomine_nid_picture_thumbnail')




admin.site.register(Account, AccountAdmin)
admin.site.register( UserProfile,  UserProfileAdmin)
