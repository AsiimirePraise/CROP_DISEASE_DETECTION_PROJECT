
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SensorDevice, SensorReading, Alert, WeatherData
from .serializers import (
    SensorDeviceSerializer, SensorReadingSerializer, SensorReadingCreateSerializer,
    AlertSerializer, WeatherDataSerializer
)


class SensorDeviceListAPIView(generics.ListAPIView):
    serializer_class = SensorDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SensorDevice.objects.filter(user=self.request.user)


class SensorReadingsAPIView(generics.ListAPIView):
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        device = get_object_or_404(SensorDevice, id=device_id, user=self.request.user)
        return SensorReading.objects.filter(device=device).order_by('-timestamp')


class SensorReadingCreateAPIView(generics.CreateAPIView):
    serializer_class = SensorReadingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Verify device belongs to user
        device = serializer.validated_data['device']
        if device.user != self.request.user:
            raise serializers.ValidationError("Device does not belong to user")
        serializer.save()


class AlertListAPIView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(rule__user=self.request.user).order_by('-created_at')


class WeatherDataAPIView(generics.ListAPIView):
    serializer_class = WeatherDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = WeatherData.objects.all().order_by('-timestamp')
        
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset[:50]  # Limit to recent 50 records
