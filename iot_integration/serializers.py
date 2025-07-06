
from rest_framework import serializers
from .models import SensorDevice, SensorReading, Alert, WeatherData


class SensorDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDevice
        fields = [
            'id', 'name', 'device_type', 'serial_number', 'location',
            'gps_coordinates', 'status', 'last_communication', 'battery_level',
            'firmware_version', 'installation_date'
        ]
        read_only_fields = ['id']


class SensorReadingSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = SensorReading
        fields = [
            'id', 'device', 'device_name', 'timestamp', 'value', 'unit',
            'quality_score', 'raw_data', 'processed', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SensorReadingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['device', 'timestamp', 'value', 'unit', 'quality_score', 'raw_data']


class AlertSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(source='rule.name', read_only=True)
    device_name = serializers.CharField(source='rule.device.name', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'rule_name', 'device_name', 'message', 'status',
            'acknowledged_by', 'acknowledged_at', 'resolved_at', 'created_at'
        ]


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            'location', 'gps_coordinates', 'timestamp', 'temperature',
            'humidity', 'precipitation', 'wind_speed', 'wind_direction',
            'pressure', 'uv_index', 'cloud_cover', 'source'
        ]
