
from django.urls import path
from . import api_views

urlpatterns = [
    path('sensors/', api_views.SensorDeviceListAPIView.as_view(), name='api_sensors'),
    path('sensors/<uuid:device_id>/readings/', api_views.SensorReadingsAPIView.as_view(), name='api_sensor_readings'),
    path('readings/', api_views.SensorReadingCreateAPIView.as_view(), name='api_create_reading'),
    path('alerts/', api_views.AlertListAPIView.as_view(), name='api_alerts'),
    path('weather/', api_views.WeatherDataAPIView.as_view(), name='api_weather'),
]
