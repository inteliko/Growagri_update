from django.contrib import admin
from .models import Post
from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    form = PostForm  # Specify the form for creating and editing Post objects
    list_display = ['title', 'author_name', 'date_posted']

admin.site.register(Post, PostAdmin)
