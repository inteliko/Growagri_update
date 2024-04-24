
from django.shortcuts import render
from django.http import HttpResponse
from farm.models import Farm
from blog.models import Post


def home(request):
    farms = Farm.objects.all().filter(is_available=True)
    posts = Post.objects.order_by('-date_posted')[:3]  # Retrieve the three most recent posts





    context ={
        'farms': farms,
        'posts': posts,

    }

    return render(request, 'home.html', context)





def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'legal/faq.html')


