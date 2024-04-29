# urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('about/', views.about, name='about-us'),
    path('faq/', views.faq, name='faq'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('risk-policy/', views.risk_policy, name='risk-policy'),
    path('return-investment/', views.return_investment, name='return-investment'),
    path('contact/', views.contact, name='contact'),







]
