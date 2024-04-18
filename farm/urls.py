# urls.py

from django.urls import path
from .import views 


urlpatterns = [

    path('', views.farm, name='farm'),
    path('slug:category_slug/', views.farm, name='farms_by_croptype'),
    path('<slug:category_slug>/<slug:farm_slug>/', views.farm_detail, name='farm_detail'),


]
