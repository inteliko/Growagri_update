from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Farm
from projects.models import CropType

# Create your views here.

def farm(request):
    farms = Farm.objects.all().filter(is_available=True)

    context ={
        'farms': farms,
    }
    return render(request, 'farm/farm.html', context)



def farm_detail(request, category_slug, farm_slug):
    farm = get_object_or_404(Farm, slug=farm_slug)
    total_sum_value = farm.calculate_roi() + farm.price
    context = {
        'farm': farm,
        'total_sum_value': total_sum_value,
    }
    return render(request, 'farm/farm_detail.html', context)