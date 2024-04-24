from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def weather_view(request):

    if request.method == 'POST':
        city = request.POST.get('city', 'indore')  # Default to 'indore' if no city is provided
        api_key = 'e3aff9dc246a6d6567ce7db04a8f4249'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
            return render(request, 'weather/weather.html', {'weather_data': weather_data})
        else:
            error_message = f'Error fetching weather data: {response.status_code}'
            return render(request, 'weather/error.html', {'error_message': error_message})
    else:
        return render(request, 'weather/weather.html')
               
    