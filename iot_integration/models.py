
from django.db import models
from django.contrib.auth import get_user_model
from diagnosis.models import Crop
import uuid

User = get_user_model()


class SensorDevice(models.Model):
    DEVICE_TYPES = [
        ('soil_moisture', 'Soil Moisture'),
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('ph_sensor', 'pH Sensor'),
        ('light_sensor', 'Light Sensor'),
        ('weather_station', 'Weather Station'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('error', 'Error'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True)
    gps_coordinates = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    last_communication = models.DateTimeField(null=True, blank=True)
    battery_level = models.FloatField(null=True, blank=True, help_text="Battery percentage")
    firmware_version = models.CharField(max_length=20, blank=True)
    installation_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_device_type_display()})"

    class Meta:
        ordering = ['-created_at']


class SensorReading(models.Model):
    device = models.ForeignKey(SensorDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()
    unit = models.CharField(max_length=20, blank=True)
    quality_score = models.FloatField(default=1.0, help_text="Data quality 0-1")
    raw_data = models.JSONField(default=dict, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.value} {self.unit} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]


class AlertRule(models.Model):
    CONDITION_TYPES = [
        ('above', 'Above Threshold'),
        ('below', 'Below Threshold'),
        ('between', 'Between Values'),
        ('rapid_change', 'Rapid Change'),
    ]

    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    device = models.ForeignKey(SensorDevice, on_delete=models.CASCADE)
    condition_type = models.CharField(max_length=15, choices=CONDITION_TYPES)
    threshold_value = models.FloatField()
    threshold_value_max = models.FloatField(null=True, blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='medium')
    is_active = models.BooleanField(default=True)
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.device.name}"


class Alert(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ]

    rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE)
    sensor_reading = models.ForeignKey(SensorReading, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    acknowledged_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.rule.name} - {self.status}"

    class Meta:
        ordering = ['-created_at']


class WeatherData(models.Model):
    location = models.CharField(max_length=200)
    gps_coordinates = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField()
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_direction = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    uv_index = models.FloatField(null=True, blank=True)
    cloud_cover = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=50, default='api')
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather at {self.location} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        unique_together = ['location', 'timestamp', 'source']


class FarmEnvironment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    gps_coordinates = models.CharField(max_length=50, blank=True)
    area_size = models.FloatField(help_text="Area in acres")
    crops = models.ManyToManyField(Crop, related_name='farm_environments')
    devices = models.ManyToManyField(SensorDevice, related_name='farm_environments', blank=True)
    soil_type = models.CharField(max_length=100, blank=True)
    irrigation_type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()}"

    class Meta:
        ordering = ['-created_at']
