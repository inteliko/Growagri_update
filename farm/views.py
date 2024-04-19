from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Farm
from projects.models import CropType

# Create your views here.

def farm(request, crop_slug=None):
    croptype = None
    farms = None

    if crop_slug:
        croptype = get_object_or_404(CropType, slug=crop_slug)
        farms = Farm.objects.filter(category=croptype, is_available=True)  # Filter by category field
        farms_count = farms.count()
    else:
        farms = Farm.objects.filter(is_available=True)
        farms_count = farms.count()

    context = {
        'croptype': croptype,
        'farms': farms,
        'farms_count': farms_count,
    }
    return render(request, 'farm/farm.html', context)



def farm_detail(request, crop_slug, farm_slug):
    farm = get_object_or_404(Farm, slug=farm_slug)
    total_sum_value = farm.calculate_roi() + farm.price
    context = {
        'farm': farm,
        'total_sum_value': total_sum_value,
    }
    return render(request, 'farm/farm_detail.html', context)