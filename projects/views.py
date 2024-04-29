
from django.shortcuts import render
from django.http import HttpResponse
from farm.models import Farm
from blog.models import Post


def home(request):
    farms = Farm.objects.filter(is_available=True)[:6]  # Retrieve the first six available farms
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

def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')

def risk_policy(request):
    return render(request, 'legal/risk_policy.html')


def return_investment(request):
    return render(request, 'legal/return_investment.html')

def contact(request):
    return render(request, 'contact.html')

def funders(request):
    return render(request, 'method/funders.html')

def farmers(request):
    return render(request, 'method/farmers.html')


