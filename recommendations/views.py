from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from diagnosis.models import diagnosis
from .models import Recommendation, SavedRecommendation
#from .forms import RecommendationForm 

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def get_weather_data(request):
    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={
                'lat': lat,
                'lon': lon,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        )
        response.raise_for_status()
        data = response.json()

        return JsonResponse({
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'conditions': data['weather'][0]['description']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)