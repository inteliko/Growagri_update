from django.db import models
from django.urls import reverse

class CropType(models.Model):
    croptype_name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=255, blank=True)
    crop_image = models.ImageField(upload_to='croptype_images/', blank=True)


    def get_url(self):
        return reverse()

    def __str__(self):
        return self.croptype_name
