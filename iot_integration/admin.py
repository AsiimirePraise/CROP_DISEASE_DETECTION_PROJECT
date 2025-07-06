
from django.contrib import admin
from .models import SensorDevice, SensorReading, AlertRule, Alert, WeatherData, FarmEnvironment


@admin.register(SensorDevice)
class SensorDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_type', 'user', 'status', 'last_communication', 'battery_level']
    list_filter = ['device_type', 'status', 'installation_date']
    search_fields = ['name', 'serial_number', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'value', 'unit', 'quality_score', 'processed']
    list_filter = ['device__device_type', 'timestamp', 'processed']
    search_fields = ['device__name']
    readonly_fields = ['created_at']


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'device', 'condition_type', 'threshold_value', 'severity', 'is_active']
    list_filter = ['condition_type', 'severity', 'is_active']
    search_fields = ['name', 'device__name', 'user__email']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['rule', 'status', 'acknowledged_by', 'created_at']
    list_filter = ['status', 'rule__severity', 'created_at']
    search_fields = ['rule__name', 'message']
    readonly_fields = ['created_at']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'timestamp', 'temperature', 'humidity', 'precipitation', 'source']
    list_filter = ['source', 'timestamp']
    search_fields = ['location']
    readonly_fields = ['created_at']


@admin.register(FarmEnvironment)
class FarmEnvironmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'location', 'area_size', 'created_at']
    search_fields = ['name', 'location', 'user__email']
    filter_horizontal = ['crops', 'devices']
    readonly_fields = ['created_at', 'updated_at']
