
from django.urls import path
from . import views

app_name = 'iot_integration'

urlpatterns = [
    path('', views.iot_dashboard_view, name='dashboard'),
    path('devices/', views.device_list_view, name='devices'),
    path('devices/<uuid:device_id>/', views.device_detail_view, name='device_detail'),
    path('devices/add/', views.device_add_view, name='device_add'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('alerts/<int:alert_id>/acknowledge/', views.acknowledge_alert_view, name='acknowledge_alert'),
    path('weather/', views.weather_view, name='weather'),
    path('environments/', views.farm_environments_view, name='environments'),
]
