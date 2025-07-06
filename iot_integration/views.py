
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import SensorDevice, SensorReading, Alert, WeatherData, FarmEnvironment


@login_required
def iot_dashboard_view(request):
    user_devices = SensorDevice.objects.filter(user=request.user)
    
    # Recent readings (last 24 hours)
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    recent_readings = SensorReading.objects.filter(
        device__user=request.user,
        timestamp__gte=twenty_four_hours_ago
    ).order_by('-timestamp')[:10]
    
    # Active alerts
    active_alerts = Alert.objects.filter(
        rule__user=request.user,
        status='active'
    ).order_by('-created_at')[:5]
    
    # Device status summary
    device_stats = {
        'total': user_devices.count(),
        'active': user_devices.filter(status='active').count(),
        'inactive': user_devices.filter(status='inactive').count(),
        'error': user_devices.filter(status='error').count(),
    }
    
    context = {
        'devices': user_devices[:5],  # Show recent 5 devices
        'recent_readings': recent_readings,
        'active_alerts': active_alerts,
        'device_stats': device_stats,
    }
    
    return render(request, 'iot_integration/dashboard.html', context)


@login_required
def device_list_view(request):
    devices = SensorDevice.objects.filter(user=request.user)
    
    return render(request, 'iot_integration/devices.html', {'devices': devices})


@login_required
def device_detail_view(request, device_id):
    device = get_object_or_404(SensorDevice, id=device_id, user=request.user)
    
    # Recent readings (last 48 hours)
    forty_eight_hours_ago = timezone.now() - timedelta(hours=48)
    readings = SensorReading.objects.filter(
        device=device,
        timestamp__gte=forty_eight_hours_ago
    ).order_by('-timestamp')
    
    context = {
        'device': device,
        'readings': readings,
    }
    
    return render(request, 'iot_integration/device_detail.html', context)


@login_required
def device_add_view(request):
    # Placeholder for device addition form
    return render(request, 'iot_integration/device_add.html')


@login_required
def alerts_view(request):
    alerts = Alert.objects.filter(rule__user=request.user).order_by('-created_at')
    
    return render(request, 'iot_integration/alerts.html', {'alerts': alerts})


@login_required
def acknowledge_alert_view(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, rule__user=request.user)
    
    if alert.status == 'active':
        alert.status = 'acknowledged'
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        messages.success(request, 'Alert acknowledged successfully.')
    
    return redirect('iot_integration:alerts')


def weather_view(request):
    # Get recent weather data
    recent_weather = WeatherData.objects.all().order_by('-timestamp')[:10]
    
    return render(request, 'iot_integration/weather.html', {'weather_data': recent_weather})


@login_required
def farm_environments_view(request):
    environments = FarmEnvironment.objects.filter(user=request.user)
    
    return render(request, 'iot_integration/environments.html', {'environments': environments})
