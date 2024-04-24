
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author_name', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'ckeditor'}),
        }
