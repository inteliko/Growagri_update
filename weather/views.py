from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import datetime


def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city', 'indore')
    else:
        city = 'Dhaka'

    api_key = 'e3aff9dc246a6d6567ce7db04a8f4249'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        forecast_data = []
        for item in data['list']:
            # Parse the datetime string into a datetime object
            datetime_str = item['dt_txt']
            forecast_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

            forecast_data.append({
                'datetime': forecast_datetime,
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            })

        return render(request, 'dashboard/weather.html', {'forecast_data': forecast_data, 'city': city})
    else:
        error_message = data.get('message', 'Unknown error')
        messages.error(request, f'Error: {error_message}')
        return redirect('weather')
