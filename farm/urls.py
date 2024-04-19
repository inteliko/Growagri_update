from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the farm view
    path('', views.farm, name='farm'),

    # URL pattern for farms filtered by crop type
    path('<slug:crop_slug>/', views.farm, name='farms_by_croptype'),

    # URL pattern for farm detail
    path('<slug:crop_slug>/<slug:farm_slug>/', views.farm_detail, name='farm_detail'),
]
