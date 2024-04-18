from django.db import models
from projects.models import CropType 
from django.core.validators import MinValueValidator


class Farm(models.Model):
    farm_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/farm')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(CropType, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    campaign_status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('completed', 'Completed')], default='draft')
    location = models.CharField(max_length=200, default='')  # Location of the farm
    duration = models.IntegerField(default=None, null=True, blank=True)
    custom_percentage = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return self.farm_name
    
    def calculate_roi(self):
        """
        Calculate the Return on Investment (ROI) based on the price and the custom percentage.
        """
        if self.custom_percentage is None:
            raise ValueError("Custom percentage is not specified.")
        
        return (self.price * self.custom_percentage) / 100

def sum_roi_and_price():
    """
    Calculate the sum of calculate_roi and price for all farms.
    """
    farms = Farm.objects.all()
    total_sum = sum((farm.calculate_roi() + farm.price) for farm in farms)
    return total_sum
